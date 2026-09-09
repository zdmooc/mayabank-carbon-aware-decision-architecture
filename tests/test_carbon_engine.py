#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "carbon-engine" / "engine.py"
spec = importlib.util.spec_from_file_location("carbon_engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class CarbonEngineTest(unittest.TestCase):
    def test_baseline_totals(self):
        result = engine.calculate_scenario(ROOT / "carbon-engine" / "scenarios" / "baseline.csv")
        self.assertAlmostEqual(result["totals"]["energy_kwh_year"], 7752.6, places=2)
        self.assertAlmostEqual(result["totals"]["emissions_kgco2e_year"], 576.715, places=2)
        self.assertAlmostEqual(result["totals"]["annual_cost_eur"], 72240.0, places=2)

    def test_optimized_totals(self):
        result = engine.calculate_scenario(ROOT / "carbon-engine" / "scenarios" / "optimized.csv")
        self.assertAlmostEqual(result["totals"]["energy_kwh_year"], 4680.975, places=2)
        self.assertAlmostEqual(result["totals"]["emissions_kgco2e_year"], 350.350, places=2)
        self.assertAlmostEqual(result["totals"]["annual_cost_eur"], 57864.0, places=2)

    def test_reduction(self):
        baseline = engine.calculate_scenario(ROOT / "carbon-engine" / "scenarios" / "baseline.csv")
        optimized = engine.calculate_scenario(ROOT / "carbon-engine" / "scenarios" / "optimized.csv")
        comparison = engine.compare(baseline, optimized)
        self.assertAlmostEqual(comparison["reduction_pct"]["energy_kwh_year"], 39.62, places=2)
        self.assertAlmostEqual(comparison["reduction_pct"]["emissions_kgco2e_year"], 39.25, places=2)
        self.assertAlmostEqual(comparison["reduction_pct"]["annual_cost_eur"], 19.90, places=2)


if __name__ == "__main__":
    unittest.main()
