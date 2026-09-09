import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from optimization.pareto import analyze, dominates, load_profile, read_rows


class MultiCriteriaTests(unittest.TestCase):
    def setUp(self):
        self.rows = read_rows()
        self.profile = load_profile()

    def test_ineligible_option_not_recommended(self):
        result = analyze()["analysis"][0]
        self.assertNotEqual(result["recommendedOption"], "OPT-INELIGIBLE")

    def test_aggressive_option_is_dominated(self):
        by_id = {row["option_id"]: row for row in self.rows}
        self.assertTrue(
            dominates(
                by_id["OPT-MIGRATE"],
                by_id["OPT-AGGRESSIVE"],
                self.profile["directions"],
            )
        )

    def test_aggressive_option_not_on_pareto_front(self):
        result = analyze()["analysis"][0]
        self.assertNotIn("OPT-AGGRESSIVE", result["paretoOptions"])

    def test_weighted_profile_recommends_migrate(self):
        result = analyze()["analysis"][0]
        self.assertEqual(result["recommendedOption"], "OPT-MIGRATE")
        self.assertEqual(result["recommendedAction"], "MIGRATE")

    def test_alternatives_are_preserved(self):
        result = analyze()["analysis"][0]
        self.assertIn("OPT-KEEP", result["paretoOptions"])
        self.assertIn("OPT-RIGHTSIZE", result["paretoOptions"])
        self.assertIn("OPT-SERVERLESS", result["paretoOptions"])

    def test_no_auto_apply(self):
        result = analyze()["analysis"][0]
        self.assertFalse(result["autoApplyAllowed"])


if __name__ == "__main__":
    unittest.main()
