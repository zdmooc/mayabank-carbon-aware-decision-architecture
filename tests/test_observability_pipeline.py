import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "observability" / "normalize_metrics.py"

spec = importlib.util.spec_from_file_location("normalize_metrics", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ObservabilityPipelineTest(unittest.TestCase):
    def setUp(self):
        self.payload = module.normalize()
        self.rows = {r["asset_id"]: r for r in self.payload["normalized"]}

    def test_known_assets_are_correlated(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual(self.rows["ASSET-PAY-001-PROD"]["application_id"], "APP-PAY-001")

    def test_stale_metric_is_flagged(self):
        row = self.rows["ASSET-PAY-001-UAT"]
        self.assertEqual(row["freshness"], "STALE")
        self.assertIn("STALE_METRIC", row["warnings"])

    def test_missing_power_is_warning_not_silent(self):
        row = self.rows["ASSET-PAY-003-TEST"]
        self.assertEqual(row["quality"], "WARN")
        self.assertIn("MISSING_POWER", row["warnings"])

    def test_unknown_asset_is_quarantined(self):
        self.assertEqual(self.payload["quarantined"], [{"asset_id": "ASSET-UNKNOWN-001", "reason": "UNKNOWN_ASSET"}])

    def test_jvm_heap_is_preserved(self):
        self.assertEqual(self.rows["ASSET-PAY-002-PROD"]["jvm_heap_pct"], 71.0)


if __name__ == "__main__":
    unittest.main()
