import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "storage" / "assess.py"
SPEC = importlib.util.spec_from_file_location("storage_assess", MODULE_PATH)
storage_assess = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(storage_assess)


class StorageAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {row["dataset_id"]: row for row in storage_assess.assess()}

    def test_critical_ledger_is_kept_hot(self):
        result = self.results["DS-PAY-LEDGER"]
        self.assertEqual(result["decision"], "KEEP")
        self.assertEqual(result["target_tier"], "HOT")
        self.assertFalse(result["auto_apply_allowed"])

    def test_analytical_history_moves_warm_and_consolidates(self):
        actions = self.results["DS-RECON-HIST"]["actions"]
        self.assertIn("MOVE_WARM", actions)
        self.assertIn("CONSOLIDATE_DB", actions)

    def test_nonprod_reconciliation_reduces_retention_and_backups(self):
        result = self.results["DS-RECON-TEST"]
        self.assertEqual(result["target_tier"], "COLD")
        self.assertEqual(result["target_retention_days"], 90)
        self.assertIn("REDUCE_BACKUP_COPIES", result["actions"])
        self.assertIn("CONSOLIDATE_DB", result["actions"])

    def test_audit_retention_is_not_shortened(self):
        result = self.results["DS-AUDIT-ARCHIVE"]
        self.assertEqual(result["current_retention_days"], result["target_retention_days"])
        self.assertNotIn("REDUCE_RETENTION", result["actions"])

    def test_optimized_rows_reduce_synthetic_cost_and_carbon(self):
        for result in self.results.values():
            if result["decision"] == "OPTIMIZE":
                self.assertGreater(result["cost_reduction_pct"], 0)
                self.assertGreater(result["carbon_reduction_pct"], 0)
                self.assertFalse(result["auto_apply_allowed"])


if __name__ == "__main__":
    unittest.main()
