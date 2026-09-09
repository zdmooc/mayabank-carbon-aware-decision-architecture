#!/usr/bin/env python3
"""Synthetic storage/data assessment for MayaBank labs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic" / "storage-assets.csv"

COEFFICIENTS = {
    "HOT": {"cost_eur_per_gb_month": 0.12, "carbon_kgco2e_per_gb_year": 0.055},
    "WARM": {"cost_eur_per_gb_month": 0.05, "carbon_kgco2e_per_gb_year": 0.025},
    "COLD": {"cost_eur_per_gb_month": 0.015, "carbon_kgco2e_per_gb_year": 0.008},
}
BACKUP = {"cost_eur_per_gb_month": 0.012, "carbon_kgco2e_per_gb_year": 0.006}
DB_INSTANCE_COST_EUR_YEAR = 600.0
DB_INSTANCE_CARBON_KG_YEAR = 25.0


def read_rows(path: Path = DATA) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def choose_tier(row: dict) -> str:
    rto = float(row["restore_rto_minutes"])
    cpu = float(row["db_cpu_utilization_pct"])
    retention = int(row["retention_days"])

    if row["criticality"] == "CRITICAL" or rto <= 60:
        return "HOT"
    if row["data_class"] == "AUDIT" and retention >= 730:
        return "COLD" if rto >= 180 else "WARM"
    if row["environment"] != "PROD" and rto >= 240:
        return "COLD"
    if row["data_class"] == "ANALYTICAL" and cpu < 25 and rto >= 120:
        return "WARM"
    if row["data_class"] == "LOG":
        return "COLD"
    return row["current_tier"]


def choose_retention(row: dict) -> int:
    current = int(row["retention_days"])
    if row["data_class"] == "AUDIT":
        return current
    if row["data_class"] == "LOG":
        return min(current, 30)
    if row["environment"] != "PROD":
        return min(current, 90)
    return current


def choose_backup_copies(row: dict) -> int:
    return {"CRITICAL": 2, "HIGH": 2, "MEDIUM": 1, "LOW": 1}[row["criticality"]]


def choose_db_instances(row: dict) -> int:
    current = int(row["db_instance_count"])
    cpu = float(row["db_cpu_utilization_pct"])
    ram = float(row["db_ram_utilization_pct"])
    if row["criticality"] != "CRITICAL" and current > 1 and cpu < 25 and ram < 35:
        return 1
    return current


def footprint(volume_gb: float, tier: str, backup_copies: int, backup_retention_days: int, db_instances: int) -> dict:
    backup_equivalent_gb = volume_gb * backup_copies * min(backup_retention_days / 365.0, 1.0)
    annual_cost = (
        volume_gb * COEFFICIENTS[tier]["cost_eur_per_gb_month"] * 12
        + backup_equivalent_gb * BACKUP["cost_eur_per_gb_month"] * 12
        + db_instances * DB_INSTANCE_COST_EUR_YEAR
    )
    annual_carbon = (
        volume_gb * COEFFICIENTS[tier]["carbon_kgco2e_per_gb_year"]
        + backup_equivalent_gb * BACKUP["carbon_kgco2e_per_gb_year"]
        + db_instances * DB_INSTANCE_CARBON_KG_YEAR
    )
    return {
        "annual_cost_eur": round(annual_cost, 2),
        "annual_carbon_kgco2e": round(annual_carbon, 3),
        "backup_equivalent_gb": round(backup_equivalent_gb, 2),
    }


def assess_row(row: dict) -> dict:
    current_volume = float(row["volume_gb"])
    current_retention = int(row["retention_days"])
    target_retention = choose_retention(row)
    target_volume = current_volume * target_retention / current_retention
    target_tier = choose_tier(row)
    target_backups = choose_backup_copies(row)
    target_db_instances = choose_db_instances(row)

    current = footprint(
        current_volume,
        row["current_tier"],
        int(row["backup_copies"]),
        int(row["backup_retention_days"]),
        int(row["db_instance_count"]),
    )
    target = footprint(
        target_volume,
        target_tier,
        target_backups,
        int(row["backup_retention_days"]),
        target_db_instances,
    )

    actions: list[str] = []
    if target_tier != row["current_tier"]:
        actions.append(f"MOVE_{target_tier}")
    if target_retention < current_retention:
        actions.append("REDUCE_RETENTION")
    if target_backups < int(row["backup_copies"]):
        actions.append("REDUCE_BACKUP_COPIES")
    if target_db_instances < int(row["db_instance_count"]):
        actions.append("CONSOLIDATE_DB")

    cost_reduction = ((current["annual_cost_eur"] - target["annual_cost_eur"]) / current["annual_cost_eur"] * 100) if current["annual_cost_eur"] else 0
    carbon_reduction = ((current["annual_carbon_kgco2e"] - target["annual_carbon_kgco2e"]) / current["annual_carbon_kgco2e"] * 100) if current["annual_carbon_kgco2e"] else 0

    return {
        "dataset_id": row["dataset_id"],
        "decision": "KEEP" if not actions else "OPTIMIZE",
        "actions": actions,
        "current_tier": row["current_tier"],
        "target_tier": target_tier,
        "current_retention_days": current_retention,
        "target_retention_days": target_retention,
        "current_db_instances": int(row["db_instance_count"]),
        "target_db_instances": target_db_instances,
        "current": current,
        "target": target,
        "cost_reduction_pct": round(cost_reduction, 2),
        "carbon_reduction_pct": round(carbon_reduction, 2),
        "reasonCodes": actions or ["POLICY_ALREADY_ALIGNED"],
        "auto_apply_allowed": False,
    }


def assess(rows: list[dict] | None = None) -> list[dict]:
    return [assess_row(row) for row in (rows or read_rows())]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = assess()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            actions = ",".join(result["actions"]) or "NONE"
            print(
                f"{result['dataset_id']}: {result['decision']} [{actions}] "
                f"cost={result['cost_reduction_pct']}% carbon={result['carbon_reduction_pct']}%"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
