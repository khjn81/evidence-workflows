from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.engine import evaluate  # noqa: E402
from evidence_workflows.io import load_json  # noqa: E402
from evidence_workflows.jira import build_dry_run_plan  # noqa: E402
from evidence_workflows.policy import resolve_policy  # noqa: E402


class JiraDryRunTests(unittest.TestCase):
    def test_plan_requires_approval_and_never_networks(self) -> None:
        case = load_json(ROOT / "scenarios" / "cases" / "P1-careful-data-analyst.json")
        result = evaluate(resolve_policy(ROOT / "policies" / case["policy"]), case["artifact"])
        plan = build_dry_run_plan(result, "DEMO-1", "draft_worklog")
        self.assertTrue(plan["requires_human_approval"])
        self.assertFalse(plan["network_call"])
        self.assertTrue(plan["does_not_infer_duration"])
        self.assertNotIn("time_spent_seconds", plan["payload"])

    def test_invalid_issue_key_is_rejected(self) -> None:
        case = load_json(ROOT / "scenarios" / "cases" / "P1-careful-data-analyst.json")
        result = evaluate(resolve_policy(ROOT / "policies" / case["policy"]), case["artifact"])
        with self.assertRaises(ValueError):
            build_dry_run_plan(result, "not-an-issue", "add_comment")
