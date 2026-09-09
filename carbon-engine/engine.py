#!/usr/bin/env python3
"""Synthetic, dependency-free Carbon Engine for MayaBank labs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "synthetic"
SCENARIO_DIR = ROOT / "carbon-engine" / "scenarios"


def read_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def indexed(rows: List[dict], key: str) -> Dict[str, dict]:
    return {row[key]: row for row in rows}


def load_inputs():
    inventory = indexed(read_csv(DATA_DIR / "inventory.csv"), "asset_id")
    metrics = indexed(read_csv(DATA_DIR / "metrics.csv"), "asset_id")
    costs = indexed(read_csv(DATA_DIR / "costs.csv"), "asset_id")
    factors = {row["region"]: row for row in read_csv(DATA_DIR / "carbon-factors.csv")}
    return inventory, metrics, costs, factors


def calculate_scenario(scenario_path: Path) -> dict:
    inventory, metrics, costs, factors = load_inputs()
    scenario_rows = read_csv(scenario_path)

    details = []
    totals = {"energy_kwh_year": 0.0, "emissions_kgco2e_year": 0.0, "annual_cost_eur": 0.0}

    for sc in scenario_rows:
        asset_id = sc["asset_id"]
        if asset_id not in inventory or asset_id not in metrics or asset_id not in costs:
            raise ValueError(f"Missing source data for {asset_id}")

        inv = inventory[asset_id]
        metric = metrics[asset_id]
        cost = costs[asset_id]

        hours = float(sc["active_hours_per_year"])
        power_multiplier = float(sc["power_multiplier"])
        cost_multiplier = float(sc["cost_multiplier"])
        region = sc["region_override"].strip() or inv["region"]

        if region not in factors:
            raise ValueError(f"Missing carbon factor for region {region}")
        if hours < 0 or hours > 8760:
            raise ValueError(f"Invalid active hours for {asset_id}: {hours}")
        if power_multiplier <= 0 or cost_multiplier < 0:
            raise ValueError(f"Invalid multiplier for {asset_id}")
        if not sc["assumption"].strip():
            raise ValueError(f"Undocumented scenario change for {asset_id}")

        observed_power_w = float(metric["power_watts"])
        adjusted_power_w = observed_power_w * power_multiplier
        energy_kwh = adjusted_power_w * hours / 1000.0
        factor = float(factors[region]["gco2e_per_kwh"])
        emissions_kg = energy_kwh * factor / 1000.0
        annual_cost = float(cost["cost_eur"]) * 12.0 * cost_multiplier

        detail = {
            "asset_id": asset_id,
            "application_id": inv["application_id"],
            "environment": inv["environment"],
            "change_type": sc["change_type"],
            "region": region,
            "active_hours_per_year": hours,
            "observed_power_w": observed_power_w,
            "adjusted_power_w": round(adjusted_power_w, 3),
            "energy_kwh_year": round(energy_kwh, 3),
            "emissions_kgco2e_year": round(emissions_kg, 3),
            "annual_cost_eur": round(annual_cost, 2),
            "assumption": sc["assumption"],
        }
        details.append(detail)

        totals["energy_kwh_year"] += energy_kwh
        totals["emissions_kgco2e_year"] += emissions_kg
        totals["annual_cost_eur"] += annual_cost

    return {
        "scenario": scenario_path.stem.upper(),
        "method": "operational-electricity-v1-synthetic",
        "totals": {key: round(value, 3 if key != "annual_cost_eur" else 2) for key, value in totals.items()},
        "assets": details,
    }


def compare(baseline: dict, target: dict) -> dict:
    out = {"baseline": baseline["totals"], "target": target["totals"], "delta": {}, "reduction_pct": {}}
    for key in baseline["totals"]:
        before = float(baseline["totals"][key])
        after = float(target["totals"][key])
        out["delta"][key] = round(after - before, 3 if key != "annual_cost_eur" else 2)
        out["reduction_pct"][key] = round(((before - after) / before) * 100.0, 2) if before else 0.0
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=["baseline", "optimized"], default="optimized")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    baseline = calculate_scenario(SCENARIO_DIR / "baseline.csv")
    selected = calculate_scenario(SCENARIO_DIR / f"{args.scenario}.csv")
    payload = selected if args.scenario == "baseline" else {
        "selected": selected,
        "comparison_vs_baseline": compare(baseline, selected),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Scenario: {selected['scenario']}")
        for key, value in selected["totals"].items():
            print(f"{key}: {value}")
        if args.scenario != "baseline":
            comp = payload["comparison_vs_baseline"]
            print("Reduction vs BASELINE:")
            for key, value in comp["reduction_pct"].items():
                print(f"  {key}: {value}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
