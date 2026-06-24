#!/usr/bin/env python3
"""Run a two-week EnergyPlus exposure-state classroom case.

The script intentionally avoids OS-specific shell commands. It locates the
EnergyPlus executable, copies a simple controlled example IDF, patches the run
period to July 8-21, generates a synthetic Hong Kong-like EPW, runs EnergyPlus,
and extracts monitored hourly outputs and thermostat setpoints to a small CSV.

Run from starter_kits/energyplus-exposure-state:
    python run_energyplus_two_week_case.py

If EnergyPlus is not on PATH, set ENERGYPLUS_EXE:
    macOS:   export ENERGYPLUS_EXE="/Applications/EnergyPlus-25-1-0/energyplus"
    Windows: $env:ENERGYPLUS_EXE="C:\\EnergyPlusV25-1-0\\energyplus.exe"
"""

from __future__ import annotations

import csv
import math
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work" / "energyplus_two_week"
OUT = ROOT / "outputs" / "energyplus_two_week"
WEATHER = WORK / "synthetic_hk_summer.epw"
MODEL = WORK / "two_week_model.idf"
PREFIX = "two_week"


RUN_PERIOD = """RunPeriod,
    Two Week Summer Check,        !- Name
    7,                            !- Begin Month
    8,                            !- Begin Day of Month
    ,                             !- Begin Year
    7,                            !- End Month
    21,                           !- End Day of Month
    ,                             !- End Year
    Tuesday,                      !- Day of Week for Start Day
    Yes,                          !- Use Weather File Holidays and Special Days
    Yes,                          !- Use Weather File Daylight Saving Period
    No,                           !- Apply Weekend Holiday Rule
    Yes,                          !- Use Weather File Rain Indicators
    Yes,                          !- Use Weather File Snow Indicators
    No;                           !- Treat Weather as Actual
"""


SIMULATION_CONTROL = """SimulationControl,
    Yes,                          !- Do Zone Sizing Calculation
    Yes,                          !- Do System Sizing Calculation
    Yes,                          !- Do Plant Sizing Calculation
    No,                           !- Run Simulation for Sizing Periods
    Yes;                          !- Run Simulation for Weather File Run Periods
"""


MONITORING_OBJECTS = """

Output:Variable,
    *,
    Site Outdoor Air Drybulb Temperature,
    Hourly;

Output:Variable,
    *,
    Zone Mean Air Temperature,
    Hourly;

Output:Variable,
    *,
    Zone Operative Temperature,
    Hourly;

Output:Variable,
    *,
    Zone Thermostat Cooling Setpoint Temperature,
    Hourly;

Output:Variable,
    *,
    Zone Thermostat Heating Setpoint Temperature,
    Hourly;

Output:Variable,
    *,
    Zone Ideal Loads Supply Air Total Cooling Energy,
    Hourly;
"""


EXAMPLE_IDF_NAMES = [
    "5ZoneAirCooled.idf",
    "5Zone_IdealLoadsAirSystems_ReturnPlenum.idf",
    "ASHRAE901_OfficeSmall_STD2019_Denver.idf",
]


def candidate_energyplus_paths() -> list[Path]:
    candidates: list[Path] = []
    env_path = os.environ.get("ENERGYPLUS_EXE")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    which = shutil.which("energyplus")
    if which:
        candidates.append(Path(which))

    system = platform.system()
    if system == "Darwin":
        candidates.extend(sorted(Path("/Applications").glob("EnergyPlus*/energyplus")))
    elif system == "Windows":
        for base in [Path("C:/"), Path("C:/Program Files")]:
            candidates.extend(sorted(base.glob("EnergyPlus*/energyplus.exe")))
    else:
        for name in ["/usr/local/bin/energyplus", "/usr/bin/energyplus"]:
            candidates.append(Path(name))

    return candidates


def find_energyplus() -> Path:
    for candidate in candidate_energyplus_paths():
        if candidate.exists() and candidate.is_file():
            return candidate

    msg = """
EnergyPlus executable not found.

Install EnergyPlus from https://energyplus.net/downloads or
https://github.com/NREL/EnergyPlus/releases, then either:

1. add EnergyPlus to PATH, or
2. set ENERGYPLUS_EXE to the executable path.

macOS example:
    export ENERGYPLUS_EXE="/Applications/EnergyPlus-25-1-0/energyplus"

Windows PowerShell example:
    $env:ENERGYPLUS_EXE="C:\\EnergyPlusV25-1-0\\energyplus.exe"
"""
    raise SystemExit(msg)


def energyplus_root(exe: Path) -> Path:
    return exe.resolve().parent


def find_example_idf(root: Path) -> Path:
    env_idf = os.environ.get("ENERGYPLUS_IDF")
    if env_idf and Path(env_idf).exists():
        return Path(env_idf).expanduser()

    example_dirs = [
        root / "ExampleFiles",
        root.parent / "ExampleFiles",
        root,
    ]
    for example_dir in example_dirs:
        for name in EXAMPLE_IDF_NAMES:
            candidate = example_dir / name
            if candidate.exists():
                return candidate

    raise SystemExit(
        "No controlled classroom example IDF found. Set ENERGYPLUS_IDF to an "
        "IDF with real heating and cooling thermostat setpoints, such as "
        "5ZoneAirCooled.idf from the EnergyPlus ExampleFiles folder."
    )


def write_synthetic_epw(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "LOCATION,Synthetic Hong Kong Summer,HKU,CHN,TMYx,450070,22.30,114.17,8.0,30.0",
        "DESIGN CONDITIONS,0",
        "TYPICAL/EXTREME PERIODS,1,Typical Summer Week,SummerExtreme,7/8,7/21",
        "GROUND TEMPERATURES,0",
        "HOLIDAYS/DAYLIGHT SAVINGS,No,0,0,0",
        "COMMENTS 1,Synthetic classroom weather for ARCH7XXX A3. Not for design compliance.",
        "COMMENTS 2,Use to test EnergyPlus CLI, system boundary, run period, and output extraction only.",
        "DATA PERIODS,1,1,Data,Sunday,1/1,12/31",
    ]

    start = datetime(2025, 1, 1, 0, 0)
    rows: list[list[object]] = []
    for hour_index in range(8760):
        dt = start + timedelta(hours=hour_index)
        hour_of_day = dt.hour + 1
        seasonal = math.sin(2 * math.pi * (dt.timetuple().tm_yday - 172) / 365)
        diurnal = math.sin(2 * math.pi * (dt.hour - 7) / 24)
        dry_bulb = 25.5 + 4.0 * max(0, seasonal) + 2.5 * diurnal
        dew_point = dry_bulb - 4.0
        rh = max(55, min(92, 78 - 10 * diurnal + 5 * seasonal))
        sun = max(0, math.sin(math.pi * (dt.hour - 6) / 12))
        ghi = round(760 * sun * (0.85 + 0.10 * seasonal), 1)
        dni = round(520 * sun * (0.80 + 0.10 * seasonal), 1)
        dhi = round(max(0, ghi - 0.55 * dni), 1)
        sky_cover = 6 if ghi < 80 else 4

        rows.append(
            [
                dt.year,
                dt.month,
                dt.day,
                hour_of_day,
                60,
                "?9?9?9?9",
                round(dry_bulb, 1),
                round(dew_point, 1),
                round(rh, 0),
                101325,
                0,
                0,
                360,
                ghi,
                dni,
                dhi,
                0,
                0,
                0,
                0,
                120,
                2.5,
                sky_cover,
                sky_cover,
                9999,
                99999,
                9,
                999999999,
                20,
                0.18,
                0,
                0,
                0.2,
                0,
                0,
            ]
        )

    with path.open("w", newline="") as f:
        for header in headers:
            f.write(header + "\n")
        writer = csv.writer(f)
        writer.writerows(rows)


def patch_idf(source: Path, target: Path) -> None:
    text = source.read_text(errors="ignore")
    patched, runperiod_count = re.subn(
        r"(?is)\bRunPeriod\s*,.*?;",
        RUN_PERIOD,
        text,
        count=1,
    )
    if runperiod_count == 0:
        patched = text.rstrip() + "\n\n" + RUN_PERIOD
    patched, sim_count = re.subn(
        r"(?is)\bSimulationControl\s*,.*?;",
        SIMULATION_CONTROL,
        patched,
        count=1,
    )
    if sim_count == 0:
        patched = patched.rstrip() + "\n\n" + SIMULATION_CONTROL
    patched = patched.rstrip() + MONITORING_OBJECTS + "\n"
    target.write_text(patched)


def run_energyplus(exe: Path) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(exe),
        "-w",
        str(WEATHER),
        "-d",
        str(OUT),
        "-p",
        PREFIX,
        "-r",
        str(MODEL),
    ]
    print("Running:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def find_energyplus_csv() -> Path:
    candidates = sorted(OUT.glob("*out.csv")) + sorted(OUT.glob("*.csv"))
    for candidate in candidates:
        if candidate.name in {"monitored_outputs.csv"}:
            continue
        try:
            with candidate.open(newline="") as f:
                header = next(csv.reader(f))
            if header and "Date/Time" in header[0]:
                return candidate
        except Exception:
            continue
    raise SystemExit("EnergyPlus ran, but no hourly CSV with Date/Time was found.")


def pick_column(header: list[str], patterns: list[str], zone_hints: list[str] | None = None) -> str | None:
    zone_hints = zone_hints or []
    for pattern in patterns:
        matches = [col for col in header if pattern.lower() in col.lower()]
        for zone_hint in zone_hints:
            for col in matches:
                if zone_hint.lower() in col.lower():
                    return col
        if matches:
            return matches[0]
    return None


def extract_monitoring_csv(source_csv: Path) -> Path:
    def in_two_week_period(value: str) -> bool:
        match = re.search(r"(\d{1,2})/(\d{1,2})", value)
        if not match:
            return False
        month = int(match.group(1))
        day = int(match.group(2))
        return month == 7 and 8 <= day <= 21

    with source_csv.open(newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        date_col = header[0]
        zone_hints = ["SPACE1-1", "CORE_ZN", "ZONE 1", "Perimeter"]
        outdoor_col = pick_column(header, ["Site Outdoor Air Drybulb Temperature"])
        zone_col = pick_column(header, ["Zone Mean Air Temperature", "Zone Air Temperature"], zone_hints)
        operative_col = pick_column(header, ["Zone Operative Temperature"], zone_hints)
        cooling_setpoint_col = pick_column(header, ["Zone Thermostat Cooling Setpoint Temperature"], zone_hints)
        heating_setpoint_col = pick_column(header, ["Zone Thermostat Heating Setpoint Temperature"], zone_hints)
        cooling_col = pick_column(header, ["Cooling Energy", "Cooling Rate"], zone_hints)

        required_columns = {
            "outdoor dry bulb": outdoor_col,
            "zone mean air temperature": zone_col,
            "zone operative temperature": operative_col,
            "cooling thermostat setpoint": cooling_setpoint_col,
            "heating thermostat setpoint": heating_setpoint_col,
        }
        missing = [label for label, column in required_columns.items() if not column]
        if missing:
            raise SystemExit(
                "The selected IDF did not produce the required monitored "
                f"columns: {', '.join(missing)}. Use a controlled stock model "
                "such as 5ZoneAirCooled.idf, or set ENERGYPLUS_IDF to an IDF "
                "with real heating and cooling thermostat setpoints."
            )

        selected = [date_col]
        for col in [
            outdoor_col,
            zone_col,
            operative_col,
            cooling_setpoint_col,
            heating_setpoint_col,
            cooling_col,
        ]:
            if col and col not in selected:
                selected.append(col)

        output = OUT / "monitored_outputs.csv"
        with output.open("w", newline="") as out_f:
            writer = csv.writer(out_f)
            writer.writerow(selected)
            for row in reader:
                if not in_two_week_period(row.get(date_col, "")):
                    continue
                writer.writerow([row.get(col, "") for col in selected])

    return output


def write_summary(exe: Path, idf: Path, extracted: Path) -> None:
    def rel(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(ROOT.resolve()))
        except Exception:
            return str(path)

    with extracted.open(newline="") as f:
        extracted_rows = list(csv.reader(f))
    data_rows = max(0, len(extracted_rows) - 1)

    errors = sorted(OUT.glob("*err")) + sorted(OUT.glob("*out.err"))
    err_file = errors[0] if errors else None
    severe_count = fatal_count = warning_count = "unknown"
    if err_file and err_file.exists():
        err_text = err_file.read_text(errors="ignore")
        severe_count = str(err_text.count("** Severe  **"))
        fatal_count = str(err_text.count("**  Fatal  **"))
        warning_count = str(err_text.count("** Warning **"))

    summary = OUT / "two_week_summary.txt"
    summary.write_text(
        "\n".join(
            [
                "ARCH7XXX A3 EnergyPlus Exposure-State Case",
                f"EnergyPlus executable: {exe}",
                f"Source IDF: {idf}",
                f"Patched model: {rel(MODEL)}",
                f"Weather file: {rel(WEATHER)}",
                "Run period: July 8 to July 21",
                f"Extracted outputs: {rel(extracted)}",
                f"Extracted hourly rows: {data_rows}",
                f"Warnings: {warning_count}",
                f"Severe errors: {severe_count}",
                f"Fatal errors: {fatal_count}",
                "",
                "Use this as an inspectable exposure-state scenario, not as a measured performance claim.",
            ]
        )
        + "\n"
    )


def plot_if_available(extracted: Path) -> None:
    try:
        (OUT / ".mplconfig").mkdir(parents=True, exist_ok=True)
        (OUT / ".cache").mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".mplconfig"))
        os.environ.setdefault("XDG_CACHE_HOME", str(OUT / ".cache"))
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib not available; skipping chart.")
        return

    with extracted.open(newline="") as f:
        rows = list(csv.reader(f))
    header_index = next((i for i, row in enumerate(rows) if row and row[0] == "Date/Time"), None)
    if header_index is None:
        return

    header = rows[header_index]
    data = rows[header_index + 1 :]
    if len(header) < 2 or not data:
        return

    def to_float(value: str) -> float | None:
        try:
            return float(value)
        except Exception:
            return None

    def parse_timestamp(value: str) -> datetime | None:
        match = re.search(r"(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})", value)
        if not match:
            return None
        month, day, hour, minute, second = [int(part) for part in match.groups()]
        if hour == 24:
            return datetime(2025, month, day, 0, minute, second) + timedelta(days=1)
        return datetime(2025, month, day, hour, minute, second)

    x_dt = [parse_timestamp(row[0]) for row in data]
    if any(value is None for value in x_dt):
        x = list(range(len(data)))
    else:
        x = x_dt

    plt.figure(figsize=(9, 4.8))

    def friendly_name(name: str) -> str:
        lower = name.lower()
        if "outdoor air drybulb" in lower:
            return "Outdoor dry bulb"
        if "zone mean air temperature" in lower:
            return "Zone air temp"
        if "zone operative temperature" in lower:
            return "Zone operative temp"
        if "cooling setpoint" in lower:
            return "Cooling setpoint"
        if "heating setpoint" in lower:
            return "Heating setpoint"
        if "cooling energy" in lower:
            return "Cooling energy"
        if "cooling rate" in lower:
            return "Cooling rate"
        return name[:44]

    def plotted_value(name: str, value: str) -> float | None:
        result = to_float(value)
        if result is None:
            return None
        lower = name.lower()
        if "setpoint" in lower and (result > 60 or result < -20):
            return None
        return result

    styles = {
        "Outdoor dry bulb": {"color": "#b8bec7", "linewidth": 1.4, "alpha": 0.9},
        "Zone air temp": {"color": "#d96b27", "linewidth": 2.2},
        "Zone operative temp": {"color": "#8a5a22", "linewidth": 1.8, "linestyle": "--", "alpha": 0.5},
        "Cooling setpoint": {"color": "#1f78b4", "linewidth": 1.6, "linestyle": "--"},
        "Heating setpoint": {"color": "#d89b2b", "linewidth": 1.4, "linestyle": ":"},
    }

    for col_idx, name in enumerate(header[1:], start=1):
        lower = name.lower()
        if "cooling energy" in lower or "cooling rate" in lower:
            continue
        label = friendly_name(name)
        values = [plotted_value(name, row[col_idx]) if col_idx < len(row) else None for row in data]
        if any(v is not None for v in values):
            plt.plot(x, values, label=label, **styles.get(label, {"linewidth": 1.4}))
    plt.title("EnergyPlus two-week exposure-state check")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature, deg C")
    plt.grid(alpha=0.25)
    if x and not isinstance(x[0], int):
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        plt.gcf().autofmt_xdate(rotation=0)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "monitored_outputs.png", dpi=180)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    exe = find_energyplus()
    root = energyplus_root(exe)
    example_idf = find_example_idf(root)

    print(f"EnergyPlus executable: {exe}")
    print(f"EnergyPlus folder: {root}")
    print(f"Example model: {example_idf}")

    write_synthetic_epw(WEATHER)
    patch_idf(example_idf, MODEL)
    run_energyplus(exe)
    source_csv = find_energyplus_csv()
    extracted = extract_monitoring_csv(source_csv)
    plot_if_available(extracted)
    write_summary(exe, example_idf, extracted)

    print(f"Wrote monitored CSV: {extracted}")
    print(f"Wrote summary: {OUT / 'two_week_summary.txt'}")
    if (OUT / "monitored_outputs.png").exists():
        print(f"Wrote chart: {OUT / 'monitored_outputs.png'}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"EnergyPlus command failed with exit code {exc.returncode}", file=sys.stderr)
        raise
