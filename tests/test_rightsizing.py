import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rightsizing" / "recommend.py"
spec = importlib.util.spec_from_file_location("rightsizing_recommend", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class RightSizingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = {r["asset_id"]: r for r in module.build_recommendations()}

    def test_critical_prod_is_guarded(self):
        rec = self.recs["ASSET-PAY-001-PROD"]
        self.assertEqual("RIGHTSIZE_DOWN", rec["action"])
        self.assertEqual(16, rec["target_vcpu"])
        self.assertEqual(60, rec["target_ram_gb"])
        self.assertTrue(rec["n_plus_one_required"])
        self.assertFalse(rec["auto_apply_allowed"])

    def test_critical_uat_respects_minimum(self):
        rec = self.recs["ASSET-PAY-001-UAT"]
        self.assertEqual("KEEP", rec["action"])
        self.assertEqual(8, rec["target_vcpu"])
        self.assertEqual(32, rec["target_ram_gb"])

    def test_high_prod_requires_more_capacity(self):
        rec = self.recs["ASSET-PAY-002-PROD"]
        self.assertEqual("RIGHTSIZE_UP", rec["action"])
        self.assertEqual(13, rec["target_vcpu"])
        self.assertEqual(49, rec["target_ram_gb"])

    def test_stale_data_blocks_recommendation(self):
        rec = self.recs["ASSET-PAY-003-TEST"]
        self.assertEqual("REVIEW_DATA", rec["action"])
        self.assertEqual("STALE_OBSERVABILITY_DATA", rec["reasonCode"])

    def test_medium_dev_can_reduce(self):
        rec = self.recs["ASSET-PAY-004-DEV"]
        self.assertEqual("RIGHTSIZE_DOWN", rec["action"])
        self.assertEqual(2, rec["target_vcpu"])
        self.assertEqual(5, rec["target_ram_gb"])


if __name__ == "__main__":
    unittest.main()
