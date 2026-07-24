from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.engine import evaluate, get_field, is_present  # noqa: E402
from evidence_workflows.io import load_json  # noqa: E402
from evidence_workflows.policy import resolve_policy  # noqa: E402


def run_case(case_id: str):
    case = load_json(ROOT / "scenarios" / "cases" / f"{case_id}.json")
    result = evaluate(
        resolve_policy(ROOT / "policies" / case["policy"]),
        case["artifact"],
    )
    return case, result


class EngineTests(unittest.TestCase):
    def test_nested_field_access_and_presence(self) -> None:
        artifact = {"next": {"owner": "Team"}, "empty": "  "}
        self.assertEqual(get_field(artifact, "next.owner"), "Team")
        self.assertIsNone(get_field(artifact, "next.due"))
        self.assertTrue(is_present(artifact["next"]))
        self.assertFalse(is_present(artifact["empty"]))

    def test_complete_case_is_ready(self) -> None:
        case, result = run_case("P1-careful-data-analyst")
        self.assertEqual(result.status, case["expected"]["status"])
        statuses = {check.check_id: check.status for check in result.checks}
        self.assertEqual(statuses["result-required-when-complete"], "pass")
        self.assertEqual(result.questions, [])

    def test_missing_fields_produce_questions_without_duplicate_field_prompts(self) -> None:
        _case, result = run_case("P2-busy-senior-engineer")
        self.assertEqual(result.status, "needs_clarification")
        fields = [question.field for question in result.questions]
        self.assertEqual(fields.count("evidence"), 1)
        self.assertEqual(fields[-2:], ["next_action.owner", "next_action.due_date"])

    def test_unverifiable_claim_remains_unknown(self) -> None:
        _case, result = run_case("P3-optimistic-manager")
        statuses = {check.check_id: check.status for check in result.checks}
        self.assertEqual(result.status, "unable_to_determine")
        self.assertEqual(statuses["evidence-reference"], "unknown")

    def test_sensitive_artifact_is_redacted_before_result(self) -> None:
        _case, result = run_case("P4-sensitive-incident-responder")
        serialized = json.dumps(result.to_dict(), ensure_ascii=False)
        self.assertEqual(result.status, "needs_clarification")
        self.assertNotIn("customer@example.com", serialized)
        self.assertNotIn("token_placeholder_12345678", serialized)
        self.assertTrue(result.redactions)

    def test_in_progress_work_has_explicit_non_applicable_result(self) -> None:
        _case, result = run_case("P5-in-progress-junior-researcher")
        statuses = {check.check_id: check.status for check in result.checks}
        self.assertEqual(result.status, "ready")
        self.assertEqual(statuses["result-required-when-complete"], "not_applicable")
        self.assertTrue(result.warnings)

    def test_invalid_date_does_not_pass(self) -> None:
        case, _result = run_case("P1-careful-data-analyst")
        artifact = dict(case["artifact"])
        artifact["next_experiment"] = dict(artifact["next_experiment"])
        artifact["next_experiment"]["due_date"] = "2026-99-99"
        result = evaluate(
            resolve_policy(ROOT / "policies" / case["policy"]),
            artifact,
        )
        statuses = {check.check_id: check.status for check in result.checks}
        self.assertEqual(statuses["next-experiment-due-date"], "unknown")
        self.assertEqual(result.status, "unable_to_determine")
