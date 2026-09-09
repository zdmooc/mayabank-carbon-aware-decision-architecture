#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic"


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


def to_float(value: str, field: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"ERROR: {field} must be numeric: {value}") from exc


def validate_inventory(rows: list[dict[str, str]]) -> tuple[set[str], set[str]]:
    require(bool(rows), "inventory.csv is empty")
    assets: set[str] = set()
    regions: set[str] = set()
    allowed_env = {"DEV", "TEST", "UAT", "PROD"}
    allowed_platform = {"PHYSICAL", "VM", "JVM", "POD", "DB"}
    allowed_hosting = {"ON_PREM", "OPENSHIFT_LOCAL", "AKS", "ARO"}
    allowed_criticality = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    for row in rows:
        asset_id = row["asset_id"]
        require(asset_id.startswith("ASSET-"), f"invalid asset_id: {asset_id}")
        require(asset_id not in assets, f"duplicate asset_id: {asset_id}")
        require(row["application_id"].startswith("APP-"), f"invalid application_id: {row['application_id']}")
        require(row["environment"] in allowed_env, f"invalid environment for {asset_id}")
        require(row["platform_type"] in allowed_platform, f"invalid platform_type for {asset_id}")
        require(row["hosting_target"] in allowed_hosting, f"invalid hosting_target for {asset_id}")
        require(row["criticality"] in allowed_criticality, f"invalid criticality for {asset_id}")
        require(to_float(row["vcpu_allocated"], "vcpu_allocated") >= 0, f"negative vCPU for {asset_id}")
        require(to_float(row["ram_gb_allocated"], "ram_gb_allocated") >= 0, f"negative RAM for {asset_id}")
        require(to_float(row["storage_gb"], "storage_gb") >= 0, f"negative storage for {asset_id}")
        require(int(row["rto_minutes"]) >= 0, f"negative RTO for {asset_id}")
        require(int(row["rpo_minutes"]) >= 0, f"negative RPO for {asset_id}")
        require(row["shutdown_allowed"].lower() in {"true", "false"}, f"invalid shutdown_allowed for {asset_id}")
        assets.add(asset_id)
        regions.add(row["region"])

    return assets, regions


def validate_metrics(rows: list[dict[str, str]], assets: set[str]) -> None:
    require(bool(rows), "metrics.csv is empty")
    allowed_measurement = {"MEASURED", "CALCULATED", "ESTIMATED"}
    for row in rows:
        asset_id = row["asset_id"]
        require(asset_id in assets, f"metrics references unknown asset: {asset_id}")
        cpu = to_float(row["cpu_utilization_pct"], "cpu_utilization_pct")
        ram = to_float(row["ram_utilization_pct"], "ram_utilization_pct")
        power = to_float(row["power_watts"], "power_watts")
        confidence = to_float(row["confidence"], "confidence")
        require(0 <= cpu <= 100, f"CPU outside 0..100 for {asset_id}")
        require(0 <= ram <= 100, f"RAM outside 0..100 for {asset_id}")
        require(power >= 0, f"negative power for {asset_id}")
        require(row["measurement_type"] in allowed_measurement, f"invalid measurement_type for {asset_id}")
        require(0 <= confidence <= 1, f"confidence outside 0..1 for {asset_id}")


def validate_carbon_factors(rows: list[dict[str, str]], regions: set[str]) -> None:
    require(bool(rows), "carbon-factors.csv is empty")
    factor_regions = set()
    for row in rows:
        require(row["carbon_factor_id"].startswith("CF-"), "invalid carbon_factor_id")
        require(to_float(row["gco2e_per_kwh"], "gco2e_per_kwh") > 0, "carbon factor must be > 0")
        require(row["factor_type"] in {"SYNTHETIC", "EXTERNAL_REFERENCE"}, "invalid factor_type")
        factor_regions.add(row["region"])
    missing = regions - factor_regions
    require(not missing, f"missing carbon factors for regions: {sorted(missing)}")


def validate_costs(rows: list[dict[str, str]], assets: set[str]) -> None:
    require(bool(rows), "costs.csv is empty")
    for row in rows:
        asset_id = row["asset_id"]
        require(asset_id in assets, f"costs references unknown asset: {asset_id}")
        require(to_float(row["cost_eur"], "cost_eur") >= 0, f"negative cost for {asset_id}")
        confidence = to_float(row["confidence"], "confidence")
        require(0 <= confidence <= 1, f"cost confidence outside 0..1 for {asset_id}")


def main() -> None:
    inventory = read_csv("inventory.csv")
    metrics = read_csv("metrics.csv")
    carbon_factors = read_csv("carbon-factors.csv")
    costs = read_csv("costs.csv")

    assets, regions = validate_inventory(inventory)
    validate_metrics(metrics, assets)
    validate_carbon_factors(carbon_factors, regions)
    validate_costs(costs, assets)

    print("Iteration 01 data validation: OK")
    print(f"Assets: {len(assets)}")
    print(f"Regions: {len(regions)}")
    print(f"Metric observations: {len(metrics)}")
    print(f"Cost observations: {len(costs)}")


if __name__ == "__main__":
    main()
