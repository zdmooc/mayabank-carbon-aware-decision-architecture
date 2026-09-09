#!/usr/bin/env python3
"""Dependency-free synthetic right-sizing engine for MayaBank labs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "synthetic" / "inventory.csv"
WORKLOAD = ROOT / "data" / "synthetic" / "workload-summary.csv"
POLICIES = ROOT / "rightsizing" / "policies.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def index(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def ceil_capacity(value: float) -> int:
    return max(1, int(math.ceil(value)))


def recommendation_for(asset: dict[str, str], workload: dict[str, str], policy: dict[str, str]) -> dict:
    current_vcpu = int(asset["vcpu_allocated"])
    current_ram = int(float(asset["ram_gb_allocated"]))
    criticality = asset["criticality"]
    environment = asset["environment"]

    n_plus_one = policy["n_plus_one_required_for_prod"].lower() == "true" and environment == "PROD"
    require_fresh = policy["require_fresh_data"].lower() == "true"

    if workload["data_quality"] not in {"GOOD", "WARN"}:
        return {
            "asset_id": asset["asset_id"],
            "action": "REVIEW_DATA",
            "reasonCode": "INVALID_DATA_QUALITY",
            "current_vcpu": current_vcpu,
            "target_vcpu": current_vcpu,
            "current_ram_gb": current_ram,
            "target_ram_gb": current_ram,
            "n_plus_one_required": n_plus_one,
        }

    if require_fresh and workload["freshness"] != "FRESH":
        return {
            "asset_id": asset["asset_id"],
            "action": "REVIEW_DATA",
            "reasonCode": "STALE_OBSERVABILITY_DATA",
            "current_vcpu": current_vcpu,
            "target_vcpu": current_vcpu,
            "current_ram_gb": current_ram,
            "target_ram_gb": current_ram,
            "n_plus_one_required": n_plus_one,
        }

    p95_cpu = float(workload["p95_cpu_pct"])
    p95_ram = float(workload["p95_ram_pct"])
    cpu_headroom = float(policy["cpu_headroom_factor"])
    ram_headroom = float(policy["ram_headroom_factor"])
    max_reduction = float(policy["max_reduction_pct"]) / 100.0
    min_vcpu = int(policy["min_vcpu"])
    min_ram = int(float(policy["min_ram_gb"]))

    cpu_demand = current_vcpu * (p95_cpu / 100.0) * cpu_headroom
    ram_demand = current_ram * (p95_ram / 100.0) * ram_headroom

    cpu_floor_from_reduction = current_vcpu * (1.0 - max_reduction)
    ram_floor_from_reduction = current_ram * (1.0 - max_reduction)

    target_vcpu = ceil_capacity(max(cpu_demand, cpu_floor_from_reduction, min_vcpu))
    target_ram = ceil_capacity(max(ram_demand, ram_floor_from_reduction, min_ram))

    if target_vcpu > current_vcpu or target_ram > current_ram:
        action = "RIGHTSIZE_UP"
        reason = "CAPACITY_HEADROOM_REQUIRED"
    elif target_vcpu < current_vcpu or target_ram < current_ram:
        action = "RIGHTSIZE_DOWN"
        reason = "SUSTAINED_UNDERUTILIZATION_WITH_GUARDRAILS"
    else:
        action = "KEEP"
        reason = "CURRENT_CAPACITY_WITHIN_POLICY"

    return {
        "asset_id": asset["asset_id"],
        "application_id": asset["application_id"],
        "environment": environment,
        "criticality": criticality,
        "action": action,
        "reasonCode": reason,
        "current_vcpu": current_vcpu,
        "target_vcpu": target_vcpu,
        "current_ram_gb": current_ram,
        "target_ram_gb": target_ram,
        "p95_cpu_pct": p95_cpu,
        "p95_ram_pct": p95_ram,
        "max_reduction_pct": float(policy["max_reduction_pct"]),
        "n_plus_one_required": n_plus_one,
        "auto_apply_allowed": False,
    }


def build_recommendations() -> list[dict]:
    inventory = index(read_csv(INVENTORY), "asset_id")
    workloads = index(read_csv(WORKLOAD), "asset_id")
    policies = index(read_csv(POLICIES), "criticality")

    recommendations = []
    for asset_id, asset in inventory.items():
        if asset_id not in workloads:
            recommendations.append({
                "asset_id": asset_id,
                "action": "REVIEW_DATA",
                "reasonCode": "MISSING_WORKLOAD_SUMMARY",
                "auto_apply_allowed": False,
            })
            continue
        if asset["criticality"] not in policies:
            raise ValueError(f"Missing policy for criticality {asset['criticality']}")
        recommendations.append(recommendation_for(asset, workloads[asset_id], policies[asset["criticality"]]))
    return recommendations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    recommendations = build_recommendations()
    if args.json:
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    else:
        for rec in recommendations:
            print(
                f"{rec['asset_id']}: {rec['action']} / {rec['reasonCode']}"
                + (f" / CPU {rec.get('current_vcpu')}->{rec.get('target_vcpu')} / RAM {rec.get('current_ram_gb')}->{rec.get('target_ram_gb')}" if 'current_vcpu' in rec else "")
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
