#!/usr/bin/env python3
"""Transparent multicriteria + Pareto engine for synthetic GreenOps scenarios."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic" / "multicriteria-options.csv"
WEIGHTS_PATH = ROOT / "optimization" / "weights.json"

CRITERIA = [
    "carbon_reduction_pct",
    "cost_reduction_pct",
    "performance_score",
    "availability_score",
    "risk_score",
]


def read_rows() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["eligible"] = row["eligible"].lower() == "true"
        for key in CRITERIA:
            row[key] = float(row[key])
    return rows


def load_profile() -> dict[str, Any]:
    return json.loads(WEIGHTS_PATH.read_text(encoding="utf-8"))


def dominates(a: dict[str, Any], b: dict[str, Any], directions: dict[str, str]) -> bool:
    at_least_as_good = True
    strictly_better = False
    for key in CRITERIA:
        av, bv = float(a[key]), float(b[key])
        if directions[key] == "maximize":
            if av < bv:
                at_least_as_good = False
                break
            if av > bv:
                strictly_better = True
        else:
            if av > bv:
                at_least_as_good = False
                break
            if av < bv:
                strictly_better = True
    return at_least_as_good and strictly_better


def pareto_front(rows: list[dict[str, Any]], directions: dict[str, str]) -> list[dict[str, Any]]:
    eligible = [row for row in rows if row["eligible"]]
    front = []
    for candidate in eligible:
        if not any(
            dominates(other, candidate, directions)
            for other in eligible
            if other["option_id"] != candidate["option_id"]
        ):
            front.append(candidate)
    return front


def utility(row: dict[str, Any], profile: dict[str, Any]) -> float:
    weights = profile["weights"]
    directions = profile["directions"]
    total = 0.0
    for key in CRITERIA:
        value = max(0.0, min(100.0, float(row[key]))) / 100.0
        normalized = value if directions[key] == "maximize" else 1.0 - value
        total += float(weights[key]) * normalized
    return round(total, 4)


def analyze() -> dict[str, Any]:
    rows = read_rows()
    profile = load_profile()
    by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_candidate[row["candidate_id"]].append(row)

    results = []
    for candidate_id, options in sorted(by_candidate.items()):
        front = pareto_front(options, profile["directions"])
        front_ids = {item["option_id"] for item in front}
        scored = []
        for row in options:
            item = dict(row)
            item["utilityScore"] = utility(row, profile) if row["eligible"] else None
            item["pareto"] = row["option_id"] in front_ids
            scored.append(item)

        eligible_scored = [item for item in scored if item["eligible"]]
        recommended = max(eligible_scored, key=lambda item: item["utilityScore"])
        results.append(
            {
                "candidateId": candidate_id,
                "profileVersion": profile["profileVersion"],
                "recommendedOption": recommended["option_id"],
                "recommendedAction": recommended["action"],
                "recommendedUtilityScore": recommended["utilityScore"],
                "paretoOptions": sorted(front_ids),
                "options": scored,
                "autoApplyAllowed": False,
            }
        )
    return {"analysis": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze()
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for result in payload["analysis"]:
            print(f"Candidate: {result['candidateId']}")
            print(f"Recommended: {result['recommendedOption']} / {result['recommendedAction']}")
            print(f"Pareto: {', '.join(result['paretoOptions'])}")
            print("autoApplyAllowed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
