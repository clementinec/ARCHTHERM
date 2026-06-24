#!/usr/bin/env python3
"""A1 Ta/RH spatial-field notebook.

Reads sampled points, interpolates air temperature and relative humidity with
inverse-distance weighting (IDW), writes a gridded CSV, and produces two field
maps with the original sample points still visible.
"""

from __future__ import annotations

import csv
import math
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_CSV = Path(os.environ.get("A1_POINTS_CSV", ROOT / "sample_points.csv"))
OUT = ROOT / "outputs"
GRID_CSV = OUT / "ta_rh_idw_grid.csv"
SUMMARY_CSV = OUT / "ta_rh_idw_summary.csv"
TA_PNG = OUT / "ta_field_idw.png"
RH_PNG = OUT / "rh_field_idw.png"

GRID_X = int(os.environ.get("A1_GRID_X", "61"))
GRID_Y = int(os.environ.get("A1_GRID_Y", "41"))
POWER = float(os.environ.get("A1_IDW_POWER", "2.0"))
PAD_M = float(os.environ.get("A1_FIELD_PAD_M", "0.25"))


def read_points(path: Path) -> list[dict[str, float | str]]:
    points: list[dict[str, float | str]] = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            points.append(
                {
                    "point_id": row["point_id"],
                    "x_m": float(row["x_m"]),
                    "y_m": float(row["y_m"]),
                    "Ta_C": float(row["Ta_C"]),
                    "RH_percent": float(row["RH_percent"]),
                    "CO2_ppm": float(row.get("CO2_ppm") or "nan"),
                    "note": row.get("note", ""),
                }
            )
    if len(points) < 4:
        raise SystemExit("A1 IDW needs at least four points to make a field hypothesis.")
    return points


def linspace(start: float, end: float, count: int) -> list[float]:
    if count <= 1:
        return [start]
    step = (end - start) / (count - 1)
    return [start + step * idx for idx in range(count)]


def idw(points: list[dict[str, float | str]], x: float, y: float, field: str, power: float = POWER) -> float:
    weighted_sum = 0.0
    weight_total = 0.0
    for point in points:
        dx = x - float(point["x_m"])
        dy = y - float(point["y_m"])
        dist = math.hypot(dx, dy)
        value = float(point[field])
        if dist < 1e-9:
            return value
        weight = 1.0 / (dist**power)
        weighted_sum += weight * value
        weight_total += weight
    return weighted_sum / weight_total


def leave_one_out_mae(points: list[dict[str, float | str]], field: str) -> float:
    errors: list[float] = []
    for idx, point in enumerate(points):
        training = points[:idx] + points[idx + 1 :]
        prediction = idw(training, float(point["x_m"]), float(point["y_m"]), field)
        errors.append(abs(prediction - float(point[field])))
    return sum(errors) / len(errors)


def grid(points: list[dict[str, float | str]]) -> tuple[list[float], list[float], list[list[dict[str, float]]]]:
    xs = [float(point["x_m"]) for point in points]
    ys = [float(point["y_m"]) for point in points]
    grid_x = linspace(min(xs) - PAD_M, max(xs) + PAD_M, GRID_X)
    grid_y = linspace(min(ys) - PAD_M, max(ys) + PAD_M, GRID_Y)
    rows: list[list[dict[str, float]]] = []
    for y in grid_y:
        row: list[dict[str, float]] = []
        for x in grid_x:
            row.append(
                {
                    "x_m": x,
                    "y_m": y,
                    "Ta_C": idw(points, x, y, "Ta_C"),
                    "RH_percent": idw(points, x, y, "RH_percent"),
                }
            )
        rows.append(row)
    return grid_x, grid_y, rows


def write_grid(rows: list[list[dict[str, float]]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with GRID_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["x_m", "y_m", "Ta_C", "RH_percent"], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            for cell in row:
                writer.writerow(
                    {
                        "x_m": f"{cell['x_m']:.3f}",
                        "y_m": f"{cell['y_m']:.3f}",
                        "Ta_C": f"{cell['Ta_C']:.3f}",
                        "RH_percent": f"{cell['RH_percent']:.3f}",
                    }
                )


def write_summary(points: list[dict[str, float | str]]) -> None:
    tas = [float(point["Ta_C"]) for point in points]
    rhs = [float(point["RH_percent"]) for point in points]
    rows = [
        ("point_count", str(len(points)), "sample size behind the field"),
        ("idw_power", f"{POWER:.2f}", "higher values make nearby points dominate"),
        ("Ta_range_C", f"{min(tas):.2f} to {max(tas):.2f}", "observed sample range"),
        ("RH_range_percent", f"{min(rhs):.1f} to {max(rhs):.1f}", "observed sample range"),
        ("Ta_leave_one_out_MAE_C", f"{leave_one_out_mae(points, 'Ta_C'):.3f}", "rough interpolation sensitivity"),
        ("RH_leave_one_out_MAE_percent", f"{leave_one_out_mae(points, 'RH_percent'):.3f}", "rough interpolation sensitivity"),
    ]
    with SUMMARY_CSV.open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["metric", "value", "meaning"])
        writer.writerows(rows)


def plot_field(
    points: list[dict[str, float | str]],
    grid_x: list[float],
    grid_y: list[float],
    rows: list[list[dict[str, float]]],
    field: str,
    label: str,
    output: Path,
    cmap: str,
) -> None:
    import matplotlib

    cache_root = Path(tempfile.gettempdir()) / "archtherm_a1_idw_mpl"
    os.environ.setdefault("MPLCONFIGDIR", str(cache_root / "mplconfig"))
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_root / "cache"))
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    values = [[cell[field] for cell in row] for row in rows]
    fig, ax = plt.subplots(figsize=(8.6, 5.7))
    image = ax.imshow(
        values,
        origin="lower",
        extent=[min(grid_x), max(grid_x), min(grid_y), max(grid_y)],
        aspect="equal",
        cmap=cmap,
    )
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(label)
    ax.scatter(
        [float(point["x_m"]) for point in points],
        [float(point["y_m"]) for point in points],
        s=42,
        facecolor="white",
        edgecolor="#202020",
        linewidth=1.1,
        zorder=3,
    )
    for point in points:
        ax.text(float(point["x_m"]) + 0.06, float(point["y_m"]) + 0.06, str(point["point_id"]), fontsize=7)
    ax.set_xlabel("x position (m)")
    ax.set_ylabel("y position (m)")
    ax.set_title(f"A1 IDW field hypothesis: {label}")
    ax.grid(color="white", alpha=0.25, linewidth=0.6)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main() -> None:
    points = read_points(INPUT_CSV)
    grid_x, grid_y, rows = grid(points)
    write_grid(rows)
    write_summary(points)
    plot_field(points, grid_x, grid_y, rows, "Ta_C", "Air temperature (deg C)", TA_PNG, "inferno")
    plot_field(points, grid_x, grid_y, rows, "RH_percent", "Relative humidity (%)", RH_PNG, "YlGnBu")
    print(f"Wrote {GRID_CSV}")
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {TA_PNG}")
    print(f"Wrote {RH_PNG}")


if __name__ == "__main__":
    main()
