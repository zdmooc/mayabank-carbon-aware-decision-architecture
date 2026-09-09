import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ai-ml" / "greenops_model.py"
SPEC = importlib.util.spec_from_file_location("greenops_model", MODULE_PATH)
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


class GreenOpsMLTests(unittest.TestCase):
    def setUp(self):
        self.results = {r["assetId"]: r for r in MODEL.evaluate_all()}

    def test_forecast_generated(self):
        result = self.results["ASSET-PAY-001-PROD"]
        self.assertEqual(result["status"], "MODEL_OK")
        self.assertGreater(result["forecastCpuPct"], 0)
        self.assertGreater(result["forecastEnergyKwhYear"], 0)

    def test_spike_detected_as_anomaly(self):
        result = self.results["ASSET-PAY-002-PROD"]
        self.assertTrue(result["anomalyDetected"])
        self.assertEqual(result["status"], "ANOMALY_REVIEW")

    def test_insufficient_history_uses_fallback(self):
        result = self.results["ASSET-PAY-003-TEST"]
        self.assertEqual(result["status"], "FALLBACK_INSUFFICIENT_HISTORY")
        self.assertEqual(result["optimizationScore"], 0.0)
        self.assertLess(result["confidenceScore"], 0.70)

    def test_ranking_prioritizes_underutilized_uat(self):
        ranked = MODEL.evaluate_all()
        self.assertEqual(ranked[0]["assetId"], "ASSET-PAY-001-UAT")

    def test_no_change_is_auto_applied(self):
        for result in MODEL.evaluate_all():
            self.assertNotIn("autoApply", result)


if __name__ == "__main__":
    unittest.main()
