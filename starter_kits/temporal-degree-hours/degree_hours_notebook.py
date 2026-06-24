#!/usr/bin/env python3
"""A3 degree-hours notebook for EnergyPlus-style hourly CSVs."""

from __future__ import annotations

import csv
import os
import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT.parent / "energyplus-exposure-state" / "outputs" / "energyplus_two_week" / "monitored_outputs.csv"
INPUT_CSV = Path(os.environ.get("A3_INPUT_CSV", DEFAULT_INPUT)).expanduser()
OUT = ROOT / "outputs"
SUMMARY_CSV = OUT / "energyplus_degree_hours_summary.csv"
TIMESERIES_CSV = OUT / "energyplus_degree_hours_timeseries.csv"
PLOT_PNG = OUT / "energyplus_degree_hours_plot.png"

VARIABLE_HINT = os.environ.get("A3_VARIABLE_HINT", "operative")
THRESHOLD_C = float(os.environ.get("A3_THRESHOLD_C", "24.0"))


def parse_timestamp(value: str) -> datetime:
    match = re.search(r"(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})", value)
    if not match:
        return datetime.fromisoformat(value)
    month, day, hour, minute, second = [int(part) for part in match.groups()]
    if hour == 24:
        return datetime(2025, month, day, 0, minute, second) + timedelta(days=1)
    return datetime(2025, month, day, hour, minute, second)


def pick_column(header: list[str], hint: str) -> str:
    preferred_patterns = {
        "operative": ["operative temperature"],
        "air": ["zone mean air temperature", "zone air temperature"],
        "outdoor": ["outdoor air drybulb", "outdoor dry bulb"],
    }.get(hint.lower(), [hint.lower()])
    for pattern in preferred_patterns:
        matches = [col for col in header if pattern in col.lower()]
        if matches:
            return matches[0]
    raise SystemExit(f"No column matching A3_VARIABLE_HINT={hint!r} found in {INPUT_CSV}")


def read_series() -> tuple[str, list[dict[str, float | datetime | str]]]:
    with INPUT_CSV.open(newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        date_col = header[0]
        value_col = pick_column(header, VARIABLE_HINT)
        rows: list[dict[str, float | datetime | str]] = []
        for row in reader:
            timestamp = parse_timestamp(row[date_col])
            value = float(row[value_col])
            exceedance = max(value - THRESHOLD_C, 0.0)
            rows.append(
                {
                    "timestamp": timestamp,
                    "source_timestamp": row[date_col],
                    "value_C": value,
                    "threshold_C": THRESHOLD_C,
                    "exceeds": 1.0 if value > THRESHOLD_C else 0.0,
                    "degree_hours": exceedance,
                }
            )
    return value_col, rows


def write_outputs(value_col: str, rows: list[dict[str, float | datetime | str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with TIMESERIES_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "source_timestamp", "variable", "value_C", "threshold_C", "exceeds", "degree_hours"],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "timestamp": row["timestamp"].isoformat(sep=" "),
                    "source_timestamp": row["source_timestamp"],
                    "variable": value_col,
                    "value_C": f"{float(row['value_C']):.3f}",
                    "threshold_C": f"{THRESHOLD_C:.3f}",
                    "exceeds": int(float(row["exceeds"])),
                    "degree_hours": f"{float(row['degree_hours']):.3f}",
                }
            )

    values = [float(row["value_C"]) for row in rows]
    failure_hours = sum(int(float(row["exceeds"])) for row in rows)
    degree_hours = sum(float(row["degree_hours"]) for row in rows)
    max_row = max(rows, key=lambda row: float(row["value_C"]))
    with SUMMARY_CSV.open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["metric", "value", "meaning"])
        writer.writerow(["input_csv", str(INPUT_CSV), "source hourly file"])
        writer.writerow(["variable", value_col, "column evaluated against the threshold"])
        writer.writerow(["threshold_C", f"{THRESHOLD_C:.3f}", "failure line for this notebook run"])
        writer.writerow(["hours", str(len(rows)), "hourly records evaluated"])
        writer.writerow(["failure_hours", str(failure_hours), "hours above threshold"])
        writer.writerow(["degree_hours", f"{degree_hours:.3f}", "accumulated degrees above threshold"])
        writer.writerow(["max_value_C", f"{max(values):.3f}", "peak value in selected variable"])
        writer.writerow(["peak_timestamp", max_row["timestamp"].isoformat(sep=" "), "when peak value occurs"])


def plot(value_col: str, rows: list[dict[str, float | datetime | str]]) -> None:
    import matplotlib

    cache_root = Path(tempfile.gettempdir()) / "archtherm_degree_hours_mpl"
    os.environ.setdefault("MPLCONFIGDIR", str(cache_root / "mplconfig"))
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_root / "cache"))
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    x = [row["timestamp"] for row in rows]
    y = [float(row["value_C"]) for row in rows]
    exceed = [max(value - THRESHOLD_C, 0.0) for value in y]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(x, y, color="#d96b27", linewidth=1.9, label=value_col)
    ax.axhline(THRESHOLD_C, color="#202020", linewidth=1.2, linestyle="--", label=f"threshold {THRESHOLD_C:.1f} deg C")
    ax.fill_between(x, THRESHOLD_C, [THRESHOLD_C + value for value in exceed], where=[value > 0 for value in exceed], color="#d96b27", alpha=0.22, label="degree-hours")
    ax.set_title("A3 degree-hours from hourly exposure-state CSV")
    ax.set_ylabel("Temperature (deg C)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, frameon=False)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=0)
    fig.tight_layout()
    fig.savefig(PLOT_PNG, dpi=180)
    plt.close(fig)


def main() -> None:
    value_col, rows = read_series()
    write_outputs(value_col, rows)
    plot(value_col, rows)
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {TIMESERIES_CSV}")
    print(f"Wrote {PLOT_PNG}")


if __name__ == "__main__":
    main()
