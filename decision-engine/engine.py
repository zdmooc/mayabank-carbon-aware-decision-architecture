#!/usr/bin/env python3
"""Vendor-neutral GreenOps Decision Engine for synthetic lab candidates."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "decision-engine" / "policies.json"
DATA_PATH = ROOT / "data" / "synthetic" / "decision-candidates.csv"


def load_policy() -> dict:
    with POLICY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_candidates() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def decide(candidate: dict, policy: dict) -> dict:
    reasons: list[str] = []
    source = candidate["source_recommendation"]
    desired = policy["sourceRecommendationMap"].get(source, "REVIEW")
    criticality = candidate["criticality"]
    rules = policy["criticalityRules"][criticality]

    if candidate["data_quality"] != policy["minimumDataQuality"]:
        reasons.append("DATA_QUALITY_INSUFFICIENT")

    ml_conf = float(candidate["ml_confidence"])
    ml_sensitive = source in {"MIGRATE", "RIGHTSIZE_DOWN", "RIGHTSIZE_UP", "CONSOLIDATE", "RETIRE"}
    if ml_sensitive and ml_conf < float(policy["minimumMlConfidence"]):
        reasons.append("ML_CONFIDENCE_INSUFFICIENT")

    if rules["requireSecurityClear"] and not as_bool(candidate["security_clear"]):
        reasons.append("SECURITY_NOT_CLEARED")

    if rules["requireBudgetApproved"] and not as_bool(candidate["budget_approved"]):
        reasons.append("BUDGET_NOT_APPROVED")

    if rules["requireRtoRpoCompatible"] and not as_bool(candidate["rto_rpo_compatible"]):
        reasons.append("RTO_RPO_INCOMPATIBLE")

    if rules["requireNoBlockingDependency"] and as_bool(candidate["blocking_dependency"]):
        reasons.append("BLOCKING_DEPENDENCY")

    if source in {"REVIEW", "REVIEW_DATA"}:
        reasons.append("SOURCE_REQUIRES_REVIEW")

    decision = "REVIEW" if reasons else desired
    if not reasons:
        reasons.append(f"POLICY_APPROVED_{decision}")

    return {
        "candidateId": candidate["candidate_id"],
        "assetId": candidate["asset_id"],
        "sourceRecommendation": source,
        "decision": decision,
        "reasonCodes": reasons,
        "policyVersion": policy["policyVersion"],
        "humanApprovalRequired": bool(rules["humanApprovalRequired"] or decision == "REVIEW"),
        "autoApplyAllowed": bool(policy["autoApplyAllowed"]),
    }


def run() -> list[dict]:
    policy = load_policy()
    return [decide(row, policy) for row in load_candidates()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = run()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for row in results:
            print(f"{row['candidateId']}: {row['decision']} / {','.join(row['reasonCodes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
