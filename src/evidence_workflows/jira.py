"""Jira-shaped dry-run plans. This module never performs network I/O."""

from __future__ import annotations

import re
from typing import Any

from .models import PolicyResult

_ISSUE_KEY = re.compile(r"^[A-Z][A-Z0-9_]+-\d+$")


def build_dry_run_plan(
    result: PolicyResult,
    issue_key: str,
    operation: str = "add_comment",
) -> dict[str, Any]:
    """Return an approval-gated plan without guessing time spent or calling Jira."""

    if not _ISSUE_KEY.fullmatch(issue_key):
        raise ValueError("issue_key must look like PROJ-123")
    if operation not in {"add_comment", "draft_worklog"}:
        raise ValueError("operation must be add_comment or draft_worklog")
    payload = {
        "policy_id": result.bundle.metadata["id"],
        "policy_version": result.bundle.metadata["version"],
        "policy_digest": result.bundle.digest,
        "status": result.status,
        "follow_up_question_count": len(result.questions),
        "comment": (
            f"Evidence workflow status: {result.status}. "
            f"Policy: {result.bundle.metadata['id']}@{result.bundle.metadata['version']}."
        ),
    }
    return {
        "plan_version": "0.1.0",
        "issue_key": issue_key,
        "operation": operation,
        "requires_human_approval": True,
        "network_call": False,
        "does_not_infer_duration": True,
        "payload": payload,
        "apply_instructions": [
            "Review the redacted artifact and policy result.",
            "Approve or edit this plan in the target system.",
            "Apply it using an authenticated connector outside this package.",
            "Read back the remote receipt and retain it separately from raw answers.",
        ],
    }
