"""Deterministic interview and policy evaluation engine."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from .models import CheckResult, InterviewQuestion, PolicyResult, ResolvedPolicyBundle
from .redaction import find_sensitive, redact_value

_ISO_DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
_URL = re.compile(r"https?://[^\s)\]}>,]+", re.I)
_JIRA_KEY = re.compile(r"\b[A-Z][A-Z0-9_]+-\d+\b")
_COMMIT = re.compile(r"\b[0-9a-f]{7,40}\b", re.I)


def get_field(artifact: dict[str, Any], field: str) -> Any:
    if field == "*":
        return artifact
    current: Any = artifact
    for part in field.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def _condition_applies(condition: dict[str, Any] | None, artifact: dict[str, Any]) -> bool:
    if condition is None:
        return True
    actual = get_field(artifact, condition["field"])
    if "equals" in condition:
        return actual == condition["equals"]
    return actual in condition["in"]


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_as_text(item) for item in value.values())
    return "" if value is None else str(value)


def _has_evidence_reference(value: Any) -> bool:
    text = _as_text(value)
    return bool(_URL.search(text) or _JIRA_KEY.search(text) or _COMMIT.search(text))


def _has_date_reference(value: Any) -> bool:
    for candidate in _ISO_DATE.findall(_as_text(value)):
        try:
            date.fromisoformat(candidate)
        except ValueError:
            continue
        return True
    return False


def _evaluate_check(check: dict[str, Any], artifact: dict[str, Any]) -> str:
    if not _condition_applies(check.get("when"), artifact):
        return "not_applicable"

    value = get_field(artifact, check["field"])
    check_type = check["type"]
    if check_type == "present":
        return "pass" if is_present(value) else "fail"
    if check_type == "evidence_reference":
        if not is_present(value):
            return "fail"
        return "pass" if _has_evidence_reference(value) else "unknown"
    if check_type == "date_reference":
        if not is_present(value):
            return "fail"
        return "pass" if _has_date_reference(value) else "unknown"
    if check_type == "conditional_present":
        return "pass" if is_present(value) else "fail"
    if check_type == "no_sensitive_data":
        return "pass" if not find_sensitive(value, check["field"]) else "fail"
    if check_type == "allowed_value":
        return "pass" if is_present(value) and value in check["values"] else "fail"
    raise ValueError(f"unsupported check type: {check_type}")


def _question_map(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {question["id"]: question for question in spec["questions"]}


def _build_questions(
    spec: dict[str, Any],
    artifact: dict[str, Any],
    checks: list[CheckResult],
) -> list[InterviewQuestion]:
    questions = _question_map(spec)
    candidates: list[tuple[int, InterviewQuestion]] = []

    def add_question(question: dict[str, Any], reason: str, priority: int) -> None:
        if not _condition_applies(question.get("when"), artifact):
            return
        candidates.append(
            (
                priority,
                InterviewQuestion(
                    question_id=question["id"],
                    field=question["field"],
                    prompt=question["prompt"],
                    required=question["required"],
                    reason=reason,
                ),
            )
        )

    for check in checks:
        if check.status not in {"fail", "unknown"}:
            continue
        question = questions.get(check.question_id or "")
        if question is not None:
            reason = check.message
            if check.status == "unknown":
                reason = f"확인 가능한 근거가 없어 판단할 수 없습니다: {check.message}"
            add_question(question, reason, 0 if check.blocking else 1)

    for question in spec["questions"]:
        if question["required"] and not is_present(get_field(artifact, question["field"])):
            add_question(question, "필수 답변이 아직 없습니다.", 0)

    unique: dict[str, tuple[int, InterviewQuestion]] = {}
    for priority, question in candidates:
        unique.setdefault(question.question_id, (priority, question))
    question_order = {question["id"]: index for index, question in enumerate(spec["questions"])}
    return [
        item[1]
        for item in sorted(
            unique.values(),
            key=lambda item: (item[0], question_order[item[1].question_id]),
        )
    ]


def evaluate(bundle: ResolvedPolicyBundle, artifact: dict[str, Any]) -> PolicyResult:
    """Evaluate an artifact without inferring facts not present in the input."""

    if not isinstance(artifact, dict):
        raise TypeError("artifact must be a JSON object")
    spec = bundle.spec
    check_results: list[CheckResult] = []
    for check in spec["checks"]:
        status = _evaluate_check(check, artifact)
        check_results.append(
            CheckResult(
                check_id=check["id"],
                check_type=check["type"],
                field=check["field"],
                status=status,
                blocking=check["blocking"],
                severity=check.get("severity", "error" if check["blocking"] else "warning"),
                message=check["message"],
                question_id=check.get("question_id"),
            )
        )

    blocking_unknown = any(check.blocking and check.status == "unknown" for check in check_results)
    blocking_fail = any(check.blocking and check.status == "fail" for check in check_results)
    if blocking_unknown:
        status = "unable_to_determine"
    elif blocking_fail:
        status = "needs_clarification"
    else:
        status = "ready"

    redacted_artifact, redactions = redact_value(artifact)
    warnings: list[str] = []
    for check in check_results:
        if check.status in {"fail", "unknown"} and not check.blocking:
            warnings.append(check.message)
    progress_warning = spec.get("progress_warning")
    if progress_warning and get_field(artifact, progress_warning["field"]) in progress_warning["values"]:
        warnings.append(progress_warning["message"])
    if redactions:
        warnings.append("민감정보 패턴은 결과 출력에서 자동 마스킹되었습니다. 원문을 외부 시스템에 전송하지 마세요.")

    return PolicyResult(
        bundle=bundle,
        status=status,
        artifact=redacted_artifact,
        checks=check_results,
        questions=_build_questions(spec, artifact, check_results),
        warnings=warnings,
        redactions=redactions,
    )
