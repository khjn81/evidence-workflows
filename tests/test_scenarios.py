from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.engine import evaluate  # noqa: E402
from evidence_workflows.evaluation import assess_case  # noqa: E402
from evidence_workflows.io import load_json  # noqa: E402
from evidence_workflows.policy import resolve_policy  # noqa: E402


class ScenarioRegressionTests(unittest.TestCase):
    def test_all_five_synthetic_cases_pass_their_quality_contract(self) -> None:
        cases = sorted((ROOT / "scenarios" / "cases").glob("*.json"))
        self.assertEqual(len(cases), 5)
        for case_path in cases:
            case = load_json(case_path)
            result = evaluate(resolve_policy(ROOT / "policies" / case["policy"]), case["artifact"])
            evaluation = assess_case(case, result.to_dict())
            self.assertTrue(evaluation["overall_pass"], evaluation)
