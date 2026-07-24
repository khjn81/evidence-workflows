from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.authoring import evaluate_authoring  # noqa: E402
from evidence_workflows.io import load_json  # noqa: E402


class AuthoringInterviewTests(unittest.TestCase):
    def test_safe_complete_intake_is_draft_ready(self) -> None:
        answers = load_json(ROOT / "scenarios" / "policy-authoring" / "leader-intake.json")
        result = evaluate_authoring(answers)
        self.assertEqual(result["status"], "draft_ready")
        self.assertEqual(result["questions"], [])
        self.assertEqual(result["risk_flags"], [])

    def test_incomplete_intake_returns_questions(self) -> None:
        result = evaluate_authoring({"purpose": "Understand the next decision."})
        self.assertEqual(result["status"], "needs_clarification")
        self.assertGreater(len(result["questions"]), 1)

    def test_surveillance_intent_requires_review(self) -> None:
        answers = {
            "purpose": "Track productivity and rank employees by effort score.",
            "minimum_evidence": ["hours"],
            "allowed_states": ["completed"],
            "unknown_behavior": "Mark as fail.",
            "privacy_boundary": "None.",
            "prohibited_inferences": ["none"],
            "action_boundary": "Auto-block low scores.",
            "owner": "Manager",
            "review_after": "2026-10-01"
        }
        result = evaluate_authoring(answers)
        self.assertEqual(result["status"], "needs_clarification")
        self.assertTrue(result["risk_flags"])
        self.assertEqual(result["questions"][-1]["id"], "risk-review")

    def test_authoring_contract_validates_list_shapes_and_review_date(self) -> None:
        answers = load_json(ROOT / "scenarios" / "policy-authoring" / "leader-intake.json")
        answers["allowed_states"] = "completed"
        answers["review_after"] = "2026-99-99"
        result = evaluate_authoring(answers)
        self.assertEqual(result["status"], "needs_clarification")
        question_ids = {question["id"] for question in result["questions"]}
        self.assertEqual(question_ids, {"allowed-states", "review-after"})
