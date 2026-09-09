#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic"
INVENTORY = DATA / "inventory.csv"
RAW = DATA / "observability-raw.csv"
REFERENCE_TIME = datetime(2026, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
FRESHNESS_MINUTES = 60


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize() -> dict:
    inventory = {r["asset_id"]: r for r in read_csv(INVENTORY)}
    normalized: list[dict] = []
    quarantined: list[dict] = []

    for row in read_csv(RAW):
        asset_id = row["asset_id"]
        if asset_id not in inventory:
            quarantined.append({"asset_id": asset_id, "reason": "UNKNOWN_ASSET"})
            continue

        inv = inventory[asset_id]
        ts = parse_ts(row["timestamp"])
        age_minutes = (REFERENCE_TIME - ts).total_seconds() / 60.0
        freshness = "FRESH" if age_minutes <= FRESHNESS_MINUTES else "STALE"

        required = ["cpu_pct", "ram_pct"]
        present_required = sum(1 for key in required if row[key].strip())
        completeness_score = present_required / len(required)

        warnings: list[str] = []
        if not row["power_watts"].strip():
            warnings.append("MISSING_POWER")
        if inv["platform_type"] == "JVM" and not row["jvm_heap_pct"].strip():
            warnings.append("MISSING_JVM_HEAP")
        if freshness == "STALE":
            warnings.append("STALE_METRIC")

        quality = "GOOD"
        if completeness_score < 1.0:
            quality = "INVALID"
        elif warnings:
            quality = "WARN"

        normalized.append(
            {
                "application_id": inv["application_id"],
                "asset_id": asset_id,
                "environment": inv["environment"],
                "platform_type": inv["platform_type"],
                "timestamp": row["timestamp"],
                "age_minutes": round(age_minutes, 1),
                "freshness": freshness,
                "cpu_pct": float(row["cpu_pct"]) if row["cpu_pct"] else None,
                "ram_pct": float(row["ram_pct"]) if row["ram_pct"] else None,
                "jvm_heap_pct": float(row["jvm_heap_pct"]) if row["jvm_heap_pct"] else None,
                "power_watts": float(row["power_watts"]) if row["power_watts"] else None,
                "source": row["source"],
                "completeness_score": round(completeness_score, 2),
                "quality": quality,
                "warnings": warnings,
            }
        )

    return {
        "reference_time": REFERENCE_TIME.isoformat().replace("+00:00", "Z"),
        "freshness_threshold_minutes": FRESHNESS_MINUTES,
        "normalized": normalized,
        "quarantined": quarantined,
    }


def main() -> int:
    payload = normalize()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
