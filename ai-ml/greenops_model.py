#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic" / "ml-workload-history.csv"


def load_history() -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    with DATA.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["asset_id"]].append(
                {
                    "period": int(row["period_index"]),
                    "cpu": float(row["cpu_pct"]),
                    "power": float(row["power_watts"]),
                    "quality": float(row["data_quality"]),
                }
            )
    for rows in grouped.values():
        rows.sort(key=lambda x: x["period"])
    return grouped


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def linear_next(values: list[float]) -> float:
    if len(values) < 2:
        return values[-1]
    slope = (values[-1] - values[0]) / (len(values) - 1)
    return values[-1] + slope


def is_anomaly(values: list[float]) -> bool:
    if len(values) < 5:
        return False
    baseline = values[:-1]
    if len(baseline) < 2:
        return False
    mean = statistics.mean(baseline)
    stdev = statistics.pstdev(baseline)
    if stdev == 0:
        return abs(values[-1] - mean) > 0
    return abs(values[-1] - mean) > 3.0 * stdev


def analyze_asset(asset_id: str, rows: list[dict]) -> dict:
    cpus = [r["cpu"] for r in rows]
    powers = [r["power"] for r in rows]
    avg_quality = statistics.mean(r["quality"] for r in rows)
    point_factor = min(1.0, len(rows) / 6.0)
    confidence = round(avg_quality * point_factor, 2)

    if len(rows) < 4:
        return {
            "assetId": asset_id,
            "modelVersion": "greenops-forecast-v1",
            "status": "FALLBACK_INSUFFICIENT_HISTORY",
            "forecastCpuPct": round(cpus[-1], 2),
            "forecastPowerWatts": round(powers[-1], 2),
            "forecastEnergyKwhYear": round(powers[-1] * 8760 / 1000.0, 2),
            "anomalyDetected": False,
            "optimizationScore": 0.0,
            "confidenceScore": confidence,
        }

    forecast_cpu = clamp(linear_next(cpus), 0.0, 100.0)
    forecast_power = max(0.0, linear_next(powers))
    anomaly = is_anomaly(cpus) or is_anomaly(powers)

    underutilization = clamp((100.0 - forecast_cpu) / 100.0, 0.0, 1.0)
    power_weight = clamp(forecast_power / 300.0, 0.0, 1.0)
    optimization_score = round((0.65 * underutilization + 0.35 * power_weight) * confidence, 4)

    if anomaly:
        status = "ANOMALY_REVIEW"
    elif confidence < 0.70:
        status = "LOW_CONFIDENCE"
    else:
        status = "MODEL_OK"

    return {
        "assetId": asset_id,
        "modelVersion": "greenops-forecast-v1",
        "status": status,
        "forecastCpuPct": round(forecast_cpu, 2),
        "forecastPowerWatts": round(forecast_power, 2),
        "forecastEnergyKwhYear": round(forecast_power * 8760 / 1000.0, 2),
        "anomalyDetected": anomaly,
        "optimizationScore": optimization_score,
        "confidenceScore": confidence,
    }


def evaluate_all() -> list[dict]:
    results = [analyze_asset(asset_id, rows) for asset_id, rows in load_history().items()]
    return sorted(results, key=lambda x: x["optimizationScore"], reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = evaluate_all()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for rank, result in enumerate(results, start=1):
            print(
                f"#{rank} {result['assetId']} | status={result['status']} | "
                f"forecastCPU={result['forecastCpuPct']}% | "
                f"forecastPower={result['forecastPowerWatts']}W | "
                f"score={result['optimizationScore']} | confidence={result['confidenceScore']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
