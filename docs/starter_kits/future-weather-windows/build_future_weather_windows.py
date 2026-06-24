#!/usr/bin/env python3
"""Build small future-weather stress-window artifacts from local CMIP CSVs.

This script reads four long hourly forecast CSVs:

- Guangzhou / SSP245
- Guangzhou / SSP585
- Phoenix / SSP245
- Phoenix / SSP585

For each city-scenario pair, it selects the hottest 14-day dry-bulb window in
2025, 2050, and 2080. The output is intentionally small enough for students to
inspect in a spreadsheet, Grasshopper, Python, or a notebook.

Set CMIP_SOURCE_ROOT when the CMIP folder is not in the default OneDrive path:

    CMIP_SOURCE_ROOT="/path/to/CMIPs" python build_future_weather_windows.py
"""

from __future__ import annotations

import csv
import math
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
SLICES = OUTPUTS / "slices"
PLOTS = OUTPUTS / "plots"

SOURCE_ROOT = Path(
    os.environ.get(
        "CMIP_SOURCE_ROOT",
        str(
            Path.home()
            / "Library/CloudStorage/OneDrive-TheUniversityOfHongKong/Drafts"
            / "HPH_Carbon_Entitlement/CMIPs"
        ),
    )
)

CITIES = ["Guangzhou", "Phoenix"]
SCENARIOS = ["ssp245", "ssp585"]
YEARS = [2025, 2050, 2080]
WINDOW_HOURS = 14 * 24
TEMP_THRESHOLD_C = 30.0
HOT_HUMID_RH_THRESHOLD = 60.0
LOW_WIND_THRESHOLD_MS = 1.0
HIGH_SOLAR_THRESHOLD_WM2 = 600.0


@dataclass
class WeatherRow:
    timestamp: datetime
    temp: float
    pressure: float
    wind_speed: float
    ghi: float
    dhi: float
    dni: float
    relative_humidity: float
    specific_humidity: float


def source_csv(city: str, scenario: str) -> Path:
    return (
        SOURCE_ROOT
        / f"CMIP6_MPI_0515_{scenario}"
        / city
        / f"forecast_{city}_CMIP6_MPI_0515_{scenario}.csv"
    )


def parse_float(row: dict[str, str], name: str) -> float:
    value = row.get(name, "")
    try:
        return float(value)
    except ValueError:
        return math.nan


def load_year(path: Path, year: int) -> list[WeatherRow]:
    if not path.exists():
        raise FileNotFoundError(path)

    result: list[WeatherRow] = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = datetime.fromisoformat(row["datetime"])
            if timestamp.year != year:
                continue
            result.append(
                WeatherRow(
                    timestamp=timestamp,
                    temp=parse_float(row, "temp"),
                    pressure=parse_float(row, "pressure"),
                    wind_speed=parse_float(row, "wind_speed"),
                    ghi=parse_float(row, "GHI"),
                    dhi=parse_float(row, "DHI"),
                    dni=parse_float(row, "DNI"),
                    relative_humidity=parse_float(row, "relative_humidity"),
                    specific_humidity=parse_float(row, "specific_humidity"),
                )
            )
    return result


def hottest_window(rows: list[WeatherRow], hours: int) -> list[WeatherRow]:
    if len(rows) < hours:
        raise ValueError(f"Need at least {hours} rows; got {len(rows)}")

    temps = [row.temp for row in rows]
    current_sum = sum(temps[:hours])
    best_sum = current_sum
    best_start = 0
    for start in range(1, len(rows) - hours + 1):
        current_sum += temps[start + hours - 1] - temps[start - 1]
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = start
    return rows[best_start : best_start + hours]


def degree_hours(rows: list[WeatherRow], threshold: float) -> float:
    return sum(max(row.temp - threshold, 0.0) for row in rows)


def count_if(rows: list[WeatherRow], predicate) -> int:
    return sum(1 for row in rows if predicate(row))


def mean(values: list[float]) -> float:
    clean = [value for value in values if not math.isnan(value)]
    return sum(clean) / len(clean) if clean else math.nan


def max_value(values: list[float]) -> float:
    clean = [value for value in values if not math.isnan(value)]
    return max(clean) if clean else math.nan


def fmt(value: float, digits: int = 3) -> str:
    if math.isnan(value):
        return ""
    return f"{value:.{digits}f}"


def write_slice(city: str, scenario: str, year: int, rows: list[WeatherRow], source: Path) -> Path:
    SLICES.mkdir(parents=True, exist_ok=True)
    output = SLICES / f"{city}_{scenario}_{year}_hot14.csv"
    with output.open("w", newline="") as f:
        fieldnames = [
            "city",
            "scenario",
            "target_year",
            "window_start",
            "window_end",
            "hour_index",
            "datetime",
            "temp_C",
            "pressure_hPa",
            "wind_speed_m_s",
            "GHI_W_m2",
            "DHI_W_m2",
            "DNI_W_m2",
            "relative_humidity_percent",
            "specific_humidity_kg_kg",
            "source_file",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        window_start = rows[0].timestamp.isoformat(sep=" ")
        window_end = rows[-1].timestamp.isoformat(sep=" ")
        for hour_index, row in enumerate(rows):
            writer.writerow(
                {
                    "city": city,
                    "scenario": scenario,
                    "target_year": year,
                    "window_start": window_start,
                    "window_end": window_end,
                    "hour_index": hour_index,
                    "datetime": row.timestamp.isoformat(sep=" "),
                    "temp_C": fmt(row.temp),
                    "pressure_hPa": fmt(row.pressure),
                    "wind_speed_m_s": fmt(row.wind_speed),
                    "GHI_W_m2": fmt(row.ghi),
                    "DHI_W_m2": fmt(row.dhi),
                    "DNI_W_m2": fmt(row.dni),
                    "relative_humidity_percent": fmt(row.relative_humidity),
                    "specific_humidity_kg_kg": fmt(row.specific_humidity, 6),
                    "source_file": source.name,
                }
            )
    return output


def summary_row(city: str, scenario: str, year: int, rows: list[WeatherRow], slice_path: Path) -> dict[str, str]:
    temps = [row.temp for row in rows]
    rhs = [row.relative_humidity for row in rows]
    winds = [row.wind_speed for row in rows]
    ghi = [row.ghi for row in rows]
    max_temp = max_value(temps)
    peak_row = max(rows, key=lambda row: row.temp)

    return {
        "city": city,
        "scenario": scenario,
        "target_year": str(year),
        "window_start": rows[0].timestamp.isoformat(sep=" "),
        "window_end": rows[-1].timestamp.isoformat(sep=" "),
        "hours": str(len(rows)),
        "mean_temp_C": fmt(mean(temps)),
        "max_temp_C": fmt(max_temp),
        "peak_temp_datetime": peak_row.timestamp.isoformat(sep=" "),
        "mean_RH_percent": fmt(mean(rhs)),
        "mean_wind_m_s": fmt(mean(winds)),
        "max_GHI_W_m2": fmt(max_value(ghi)),
        "hours_temp_ge_30C": str(count_if(rows, lambda row: row.temp >= TEMP_THRESHOLD_C)),
        "degree_hours_above_30C": fmt(degree_hours(rows, TEMP_THRESHOLD_C)),
        "hot_humid_hours_temp_ge_30C_RH_ge_60": str(
            count_if(rows, lambda row: row.temp >= TEMP_THRESHOLD_C and row.relative_humidity >= HOT_HUMID_RH_THRESHOLD)
        ),
        "hot_still_hours_temp_ge_30C_wind_le_1ms": str(
            count_if(rows, lambda row: row.temp >= TEMP_THRESHOLD_C and row.wind_speed <= LOW_WIND_THRESHOLD_MS)
        ),
        "hot_sunny_hours_temp_ge_30C_GHI_ge_600": str(
            count_if(rows, lambda row: row.temp >= TEMP_THRESHOLD_C and row.ghi >= HIGH_SOLAR_THRESHOLD_WM2)
        ),
        "slice_file": str(slice_path.relative_to(ROOT)),
    }


def write_outputs(summaries: list[dict[str, str]], combined_rows: list[dict[str, str]]) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    summary_path = OUTPUTS / "future_weather_hot14_summary.csv"
    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)

    combined_path = OUTPUTS / "future_weather_hot14_slices.csv"
    with combined_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(combined_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(combined_rows)


def read_slice_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_plots(summaries: list[dict[str, str]]) -> None:
    try:
        PLOTS.mkdir(parents=True, exist_ok=True)
        cache_root = Path(tempfile.gettempdir()) / "archtherm_future_weather_mpl"
        os.environ.setdefault("MPLCONFIGDIR", str(cache_root / "mplconfig"))
        os.environ.setdefault("XDG_CACHE_HOME", str(cache_root / "cache"))
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return

    colors = {2025: "#577590", 2050: "#f8961e", 2080: "#d62828"}
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.4), sharex=True, sharey=False)

    for row_axis, city in enumerate(CITIES):
        for col_axis, scenario in enumerate(SCENARIOS):
            ax = axes[row_axis][col_axis]
            for year in YEARS:
                slice_path = SLICES / f"{city}_{scenario}_{year}_hot14.csv"
                rows = read_slice_rows(slice_path)
                x = [int(row["hour_index"]) for row in rows]
                y = [float(row["temp_C"]) for row in rows]
                ax.plot(x, y, label=str(year), color=colors[year], linewidth=1.7)
            ax.axhline(TEMP_THRESHOLD_C, color="#333333", linewidth=1.0, linestyle="--", alpha=0.55)
            ax.set_title(f"{city} / {scenario.upper()}", fontsize=11)
            ax.grid(alpha=0.22)
            ax.set_xlim(0, WINDOW_HOURS - 1)
            if col_axis == 0:
                ax.set_ylabel("Dry-bulb temp (deg C)")
            if row_axis == 1:
                ax.set_xlabel("Hour in hottest 14-day window")
            ax.legend(title="Year", fontsize=8, title_fontsize=8, frameon=False)

    fig.suptitle("Hottest 14-day weather windows from CMIP6-derived hourly files", fontsize=14)
    fig.tight_layout()
    fig.savefig(PLOTS / "future_weather_hot14_temp_profiles.png", dpi=180)
    plt.close(fig)

    labels = [f"{row['city']}\n{row['scenario'].upper()}\n{row['target_year']}" for row in summaries]
    values = [float(row["degree_hours_above_30C"]) for row in summaries]
    bar_colors = [colors[int(row["target_year"])] for row in summaries]
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.bar(range(len(values)), values, color=bar_colors)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels, rotation=0, fontsize=7)
    ax.set_ylabel("Degree-hours above 30 deg C")
    ax.set_title("Future-weather burden comparison from selected 14-day windows")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(PLOTS / "future_weather_hot14_degree_hours.png", dpi=180)
    plt.close(fig)


def main() -> None:
    summaries: list[dict[str, str]] = []
    combined_rows: list[dict[str, str]] = []

    for city in CITIES:
        for scenario in SCENARIOS:
            source = source_csv(city, scenario)
            for year in YEARS:
                rows = load_year(source, year)
                window = hottest_window(rows, WINDOW_HOURS)
                slice_path = write_slice(city, scenario, year, window, source)
                summaries.append(summary_row(city, scenario, year, window, slice_path))
                combined_rows.extend(read_slice_rows(slice_path))

    write_outputs(summaries, combined_rows)
    write_plots(summaries)

    print(f"Wrote {len(summaries)} stress-window summaries to {OUTPUTS / 'future_weather_hot14_summary.csv'}")
    print(f"Wrote combined slice table to {OUTPUTS / 'future_weather_hot14_slices.csv'}")
    print(f"Wrote individual slices to {SLICES}")


if __name__ == "__main__":
    main()
