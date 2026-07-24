"""Small, serializable domain models used by the policy engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ResolvedPolicyBundle:
    """A validated policy plus the identity of the engine that resolved it."""

    policy: dict[str, Any]
    policy_path: str
    digest: str
    engine_version: str

    @property
    def metadata(self) -> dict[str, Any]:
        return self.policy["metadata"]

    @property
    def spec(self) -> dict[str, Any]:
        return self.policy["spec"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.metadata["id"],
            "policy_version": self.metadata["version"],
            "policy_digest": self.digest,
            "engine_version": self.engine_version,
        }


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    check_type: str
    field: str
    status: str
    blocking: bool
    severity: str
    message: str
    question_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.check_id,
            "type": self.check_type,
            "field": self.field,
            "status": self.status,
            "blocking": self.blocking,
            "severity": self.severity,
            "message": self.message,
        }
        if self.question_id:
            result["question_id"] = self.question_id
        return result


@dataclass(frozen=True)
class InterviewQuestion:
    question_id: str
    field: str
    prompt: str
    required: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.question_id,
            "field": self.field,
            "prompt": self.prompt,
            "required": self.required,
            "reason": self.reason,
        }


@dataclass
class PolicyResult:
    bundle: ResolvedPolicyBundle
    status: str
    artifact: dict[str, Any]
    checks: list[CheckResult] = field(default_factory=list)
    questions: list[InterviewQuestion] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    redactions: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.bundle.to_dict(),
            "status": self.status,
            "artifact": self.artifact,
            "checks": [check.to_dict() for check in self.checks],
            "questions": [question.to_dict() for question in self.questions],
            "warnings": self.warnings,
            "redactions": self.redactions,
            "raw_input_retained": False,
        }
