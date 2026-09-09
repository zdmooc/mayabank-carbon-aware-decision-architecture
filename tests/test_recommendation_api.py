import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_PATH = ROOT / "api" / "reference_recommendation_api.py"

spec = importlib.util.spec_from_file_location("reference_recommendation_api", API_PATH)
api = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(api)


class RecommendationApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        api.AUDIT_PATH = Path(self.tmp.name) / "events.jsonl"
        api.RECOMMENDATIONS.clear()

    def tearDown(self):
        self.tmp.cleanup()

    def candidate(self, **overrides):
        data = {
            "candidate_id": "CAND-I10-1",
            "asset_id": "asset-uat-01",
            "source_recommendation": "RIGHTSIZE_DOWN",
            "criticality": "LOW",
            "data_quality": "GOOD",
            "ml_confidence": 0.91,
            "security_clear": True,
            "budget_approved": False,
            "rto_rpo_compatible": True,
            "blocking_dependency": False,
        }
        data.update(overrides)
        return data

    def test_evaluate_rightsize(self):
        result = api.evaluate(self.candidate(), "COR-I10")
        self.assertEqual(result["decision"], "RIGHTSIZE")
        self.assertTrue(result["humanApprovalRequired"])
        self.assertFalse(result["autoApplyAllowed"])
        self.assertEqual(result["correlationId"], "COR-I10")

    def test_security_gate_forces_review(self):
        result = api.evaluate(self.candidate(security_clear=False), "COR-SEC")
        self.assertEqual(result["decision"], "REVIEW")
        self.assertIn("SECURITY_NOT_CLEARED", result["reasonCodes"])

    def test_approval_never_applies_change(self):
        result = api.evaluate(self.candidate(), "COR-APP")
        approval = api.approve(
            result["recommendationId"],
            {"approvedBy": "synthetic-architect", "comment": "lab approval"},
            "COR-APP",
        )
        self.assertEqual(approval["approvalStatus"], "APPROVED")
        self.assertFalse(approval["autoApplyAllowed"])
        self.assertFalse(approval["changeApplied"])
        text = api.AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("RecommendationGenerated", text)
        self.assertIn("DecisionApproved", text)
        self.assertNotIn('"eventType": "ChangeApplied"', text)


if __name__ == "__main__":
    unittest.main()
