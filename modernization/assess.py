#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic"
CARBON_FACTOR_KG_PER_KWH = 0.075  # synthetic 75 gCO2e/kWh


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def annual_metrics(power_w: float, hours: float, monthly_cost: float) -> dict:
    energy = power_w * hours / 1000.0
    emissions = energy * CARBON_FACTOR_KG_PER_KWH
    return {
        "energy_kwh_year": round(energy, 3),
        "emissions_kgco2e_year": round(emissions, 3),
        "annual_cost_eur": round(monthly_cost * 12.0, 2),
    }


def assess() -> dict:
    source = {row["workload_id"]: row for row in read_csv(DATA / "middleware-source.csv")}
    target = {row["workload_id"]: row for row in read_csv(DATA / "openshift-target.csv")}

    results = []
    totals = {
        "source_energy_kwh_year": 0.0,
        "target_energy_kwh_year": 0.0,
        "source_emissions_kgco2e_year": 0.0,
        "target_emissions_kgco2e_year": 0.0,
        "source_annual_cost_eur": 0.0,
        "target_annual_cost_eur": 0.0,
    }

    for workload_id, src in source.items():
        if workload_id not in target:
            raise ValueError(f"Missing OpenShift target for {workload_id}")
        tgt = target[workload_id]

        src_m = annual_metrics(float(src["modeled_power_w"]), float(src["active_hours_year"]), float(src["monthly_cost_eur"]))
        tgt_m = annual_metrics(float(tgt["modeled_power_w"]), float(tgt["active_hours_year"]), float(tgt["monthly_cost_eur"]))

        risk = int(tgt["migration_risk_score"])
        blocker = tgt["blocking_dependency"].strip()
        critical = src["criticality"] in {"CRITICAL", "HIGH"}
        min_replicas = int(tgt["min_replicas"])
        pdb = int(tgt["pdb_min_available"])

        if blocker and blocker != "NONE":
            decision = "REVIEW"
            reason = blocker
        elif critical and (min_replicas < 2 or pdb < 1):
            decision = "REVIEW"
            reason = "HA_GUARDRAIL_NOT_MET"
        elif risk >= 60:
            decision = "REVIEW"
            reason = "MIGRATION_RISK_HIGH"
        else:
            decision = "MIGRATE"
            reason = "TARGET_GUARDRAILS_MET"

        energy_reduction = round(((src_m["energy_kwh_year"] - tgt_m["energy_kwh_year"]) / src_m["energy_kwh_year"]) * 100.0, 2)
        cost_reduction = round(((src_m["annual_cost_eur"] - tgt_m["annual_cost_eur"]) / src_m["annual_cost_eur"]) * 100.0, 2)

        results.append({
            "workload_id": workload_id,
            "name": src["name"],
            "decision": decision,
            "reasonCode": reason,
            "migrationRiskScore": risk,
            "source": src_m,
            "target": tgt_m,
            "energyReductionPct": energy_reduction,
            "costReductionPct": cost_reduction,
            "namespace": tgt["namespace"],
            "minReplicas": min_replicas,
            "pdbMinAvailable": pdb,
            "blockingDependency": blocker,
        })

        totals["source_energy_kwh_year"] += src_m["energy_kwh_year"]
        totals["target_energy_kwh_year"] += tgt_m["energy_kwh_year"]
        totals["source_emissions_kgco2e_year"] += src_m["emissions_kgco2e_year"]
        totals["target_emissions_kgco2e_year"] += tgt_m["emissions_kgco2e_year"]
        totals["source_annual_cost_eur"] += src_m["annual_cost_eur"]
        totals["target_annual_cost_eur"] += tgt_m["annual_cost_eur"]

    for key in totals:
        totals[key] = round(totals[key], 3 if "cost" not in key else 2)

    totals["energyReductionPct"] = round(
        ((totals["source_energy_kwh_year"] - totals["target_energy_kwh_year"]) / totals["source_energy_kwh_year"]) * 100.0, 2
    )
    totals["emissionsReductionPct"] = round(
        ((totals["source_emissions_kgco2e_year"] - totals["target_emissions_kgco2e_year"]) / totals["source_emissions_kgco2e_year"]) * 100.0, 2
    )
    totals["costReductionPct"] = round(
        ((totals["source_annual_cost_eur"] - totals["target_annual_cost_eur"]) / totals["source_annual_cost_eur"]) * 100.0, 2
    )

    return {
        "method": "synthetic-middleware-modernization-v1",
        "carbonFactorKgPerKwh": CARBON_FACTOR_KG_PER_KWH,
        "totals": totals,
        "workloads": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = assess()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for row in result["workloads"]:
            print(f"{row['workload_id']} {row['name']}: {row['decision']} ({row['reasonCode']})")
        print("Totals:")
        for key, value in result["totals"].items():
            print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
