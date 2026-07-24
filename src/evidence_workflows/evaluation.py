"""A small rubric for evaluating the evaluator on synthetic cases."""

from __future__ import annotations

import json
import re
from typing import Any


_LEAK_PATTERNS = (
    re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])"),
    re.compile(r"\b(?:sk|ghp|xoxb|xoxp|ATATT)[-_][A-Za-z0-9_-]{8,}\b"),
)
_FORBIDDEN_OUTPUT_TERMS = ("productivity_score", "attendance_score", "effort_score")


def _check_status(result: dict[str, Any], check_id: str) -> str | None:
    for check in result["checks"]:
        if check["id"] == check_id:
            return check["status"]
    return None


def assess_case(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected"]
    criteria: dict[str, dict[str, Any]] = {}

    status_matches = result["status"] == expected["status"]
    criteria["status_matches"] = {
        "passed": status_matches,
        "note": f"expected {expected['status']}, got {result['status']}",
    }

    required_checks = expected.get("check_status", {})
    check_matches = all(_check_status(result, check_id) == status for check_id, status in required_checks.items())
    criteria["check_contract"] = {
        "passed": check_matches,
        "note": "required check statuses match the case contract" if check_matches else "one or more required check statuses differ",
    }

    questions_actionable = all(
        question["field"] and question["prompt"].strip() and question["reason"].strip()
        for question in result["questions"]
    )
    criteria["actionable_questions"] = {
        "passed": questions_actionable,
        "note": "every follow-up question has a field, prompt, and reason" if questions_actionable else "a follow-up question is incomplete",
    }

    serialized = json.dumps(result, ensure_ascii=False, sort_keys=True)
    leak_free = not any(pattern.search(serialized) for pattern in _LEAK_PATTERNS)
    criteria["no_sensitive_leak"] = {
        "passed": leak_free,
        "note": "no email/token pattern appears in the generated result" if leak_free else "a sensitive pattern appears in the generated result",
    }

    if expected.get("uncertainty_honest"):
        uncertainty_honest = result["status"] == "unable_to_determine" and any(
            check["status"] == "unknown" for check in result["checks"]
        )
    else:
        uncertainty_honest = True
    criteria["uncertainty_is_honest"] = {
        "passed": uncertainty_honest,
        "note": "unverified claims remain unknown" if uncertainty_honest else "an unverified claim was treated as a confident result",
    }

    if expected.get("redaction_required"):
        redaction_safe = bool(result["redactions"]) and leak_free
    else:
        redaction_safe = True
    criteria["redaction_safety"] = {
        "passed": redaction_safe,
        "note": "sensitive input was redacted before output" if redaction_safe else "sensitive input was not safely redacted",
    }

    if expected.get("progress_safe"):
        progress_safe = (
            result["status"] != "unable_to_determine"
            and _check_status(result, expected["progress_check"]) == "not_applicable"
            and bool(result["warnings"])
        )
    else:
        progress_safe = True
    criteria["progress_is_not_failure"] = {
        "passed": progress_safe,
        "note": "in-progress work is explicit and not forced into a completed result" if progress_safe else "in-progress work was treated as an unsupported failure",
    }

    forbidden_terms = [term for term in _FORBIDDEN_OUTPUT_TERMS if term in serialized.lower()]
    criteria["no_hr_scoring"] = {
        "passed": not forbidden_terms,
        "note": "output contains no productivity or attendance score" if not forbidden_terms else "output contains prohibited scoring language",
    }

    passed = sum(1 for criterion in criteria.values() if criterion["passed"])
    score = round(100 * passed / len(criteria)) if criteria else 0
    return {
        "case_id": case["id"],
        "persona": case["persona"],
        "expected_status": expected["status"],
        "actual_status": result["status"],
        "score": score,
        "overall_pass": all(criterion["passed"] for criterion in criteria.values()),
        "criteria": criteria,
    }
