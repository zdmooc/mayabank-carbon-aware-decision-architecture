import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("modernization", ROOT / "modernization" / "assess.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class ModernizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MOD.assess()
        cls.by_id = {row["workload_id"]: row for row in cls.result["workloads"]}

    def test_stateless_critical_workload_can_migrate(self):
        row = self.by_id["MW-001"]
        self.assertEqual("MIGRATE", row["decision"])
        self.assertGreaterEqual(row["minReplicas"], 2)
        self.assertGreaterEqual(row["pdbMinAvailable"], 1)

    def test_nonprod_batch_can_migrate(self):
        self.assertEqual("MIGRATE", self.by_id["MW-002"]["decision"])

    def test_local_session_state_requires_review(self):
        row = self.by_id["MW-003"]
        self.assertEqual("REVIEW", row["decision"])
        self.assertEqual("EXTERNALIZE_SESSION_STATE", row["reasonCode"])

    def test_target_reduces_modeled_energy(self):
        totals = self.result["totals"]
        self.assertLess(totals["target_energy_kwh_year"], totals["source_energy_kwh_year"])
        self.assertGreater(totals["energyReductionPct"], 0)

    def test_target_reduces_synthetic_cost(self):
        totals = self.result["totals"]
        self.assertLess(totals["target_annual_cost_eur"], totals["source_annual_cost_eur"])
        self.assertGreater(totals["costReductionPct"], 0)


if __name__ == "__main__":
    unittest.main()
