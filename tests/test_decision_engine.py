import csv
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "decision-engine" / "engine.py"
spec = importlib.util.spec_from_file_location("decision_engine", MODULE)
engine = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(engine)


class DecisionEngineTests(unittest.TestCase):
    def test_expected_decisions(self):
        results = {row["candidateId"]: row for row in engine.run()}
        with (ROOT / "data" / "synthetic" / "decision-candidates.csv").open("r", encoding="utf-8", newline="") as handle:
            candidates = list(csv.DictReader(handle))
        for candidate in candidates:
            self.assertEqual(results[candidate["candidate_id"]]["decision"], candidate["expected_decision"])

    def test_security_block_forces_review(self):
        row = {r["candidateId"]: r for r in engine.run()}["CAND-006"]
        self.assertEqual(row["decision"], "REVIEW")
        self.assertIn("SECURITY_NOT_CLEARED", row["reasonCodes"])

    def test_bad_data_forces_review(self):
        row = {r["candidateId"]: r for r in engine.run()}["CAND-007"]
        self.assertEqual(row["decision"], "REVIEW")
        self.assertIn("DATA_QUALITY_INSUFFICIENT", row["reasonCodes"])

    def test_blocking_dependency_forces_review(self):
        row = {r["candidateId"]: r for r in engine.run()}["CAND-008"]
        self.assertIn("BLOCKING_DEPENDENCY", row["reasonCodes"])

    def test_no_auto_apply(self):
        for row in engine.run():
            self.assertFalse(row["autoApplyAllowed"])
            self.assertTrue(row["humanApprovalRequired"])


if __name__ == "__main__":
    unittest.main()
