"""The policy-authoring interview that precedes executable policy packs."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from .redaction import redact_value


AUTHORING_QUESTIONS: tuple[dict[str, Any], ...] = (
    {
        "id": "purpose",
        "field": "purpose",
        "prompt": "이 artifact가 지원할 의사결정 또는 협업 문제는 무엇인가요?",
        "required": True,
    },
    {
        "id": "minimum-evidence",
        "field": "minimum_evidence",
        "prompt": "결정을 위해 반드시 필요한 최소 증거는 무엇인가요?",
        "required": True,
    },
    {
        "id": "allowed-states",
        "field": "allowed_states",
        "prompt": "진행 중, 완료, blocked 등 어떤 lifecycle 상태를 허용하나요?",
        "required": True,
    },
    {
        "id": "unknown-behavior",
        "field": "unknown_behavior",
        "prompt": "증거가 없거나 검증할 수 없을 때 어떻게 표시하고 어떤 질문을 할까요?",
        "required": True,
    },
    {
        "id": "privacy-boundary",
        "field": "privacy_boundary",
        "prompt": "수집하지 않을 개인정보와 credential, 보존/삭제 경계는 무엇인가요?",
        "required": True,
    },
    {
        "id": "prohibited-inferences",
        "field": "prohibited_inferences",
        "prompt": "이 정책이 추론하거나 점수화해서는 안 되는 것은 무엇인가요?",
        "required": True,
    },
    {
        "id": "action-boundary",
        "field": "action_boundary",
        "prompt": "결과가 downstream 시스템에 어떤 행동을 제안할 수 있고, 무엇은 반드시 사람 승인이 필요한가요?",
        "required": True,
    },
    {
        "id": "owner",
        "field": "owner",
        "prompt": "정책의 책임자 또는 유지보수 팀은 누구인가요?",
        "required": True,
    },
    {
        "id": "review-after",
        "field": "review_after",
        "prompt": "정책을 다시 검토할 날짜를 ISO 날짜로 적어 주세요.",
        "required": True,
    },
)

_RISK_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "employee_scoring_or_surveillance",
        re.compile(
            r"(?:productivity|attendance|timesheet|work hours|effort score|rank employees|employee score|감시|근태|생산성 점수|노력 점수)",
            re.I,
        ),
        "사람의 생산성·근태·노력을 측정하거나 인사 점수로 사용할 의도가 보입니다.",
    ),
    (
        "hidden_criteria",
        re.compile(r"(?:secret criteria|hidden standard|말하지 않고|알아서 눈치|비공개 기준)", re.I),
        "답변자가 알 수 없는 숨은 기준은 정책 계약으로 허용하지 않습니다.",
    ),
)


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_as_text(item) for item in value.values())
    return "" if value is None else str(value)


def evaluate_authoring(answers: dict[str, Any]) -> dict[str, Any]:
    """Evaluate whether a leader intake is safe and complete enough to review."""

    if not isinstance(answers, dict):
        raise TypeError("authoring answers must be a JSON object")
    questions: list[dict[str, Any]] = []
    list_fields = {"minimum_evidence", "allowed_states", "prohibited_inferences"}
    for question in AUTHORING_QUESTIONS:
        field = question["field"]
        value = answers.get(field)
        reason: str | None = None
        if not _present(value):
            reason = "정책을 공개적으로 검토하기 전에 필요한 답변입니다."
        elif field in list_fields and (
            not isinstance(value, list)
            or not value
            or not all(isinstance(item, str) and item.strip() for item in value)
        ):
            reason = "이 항목은 비어 있지 않은 문자열 배열이어야 합니다."
        elif field == "review_after":
            try:
                date.fromisoformat(str(value))
            except ValueError:
                reason = "검토일은 유효한 ISO 날짜여야 합니다."
        if reason:
            questions.append(
                {
                    **question,
                    "reason": reason,
                }
            )

    risk_flags: list[dict[str, str]] = []
    intent_text = " ".join(
        _as_text(answers.get(field))
        for field in ("purpose", "minimum_evidence", "action_boundary")
    )
    for code, pattern, message in _RISK_PATTERNS:
        if pattern.search(intent_text):
            risk_flags.append({"code": code, "message": message})

    prohibited = answers.get("prohibited_inferences")
    if isinstance(prohibited, list):
        prohibited_text = " ".join(_as_text(item).casefold() for item in prohibited)
        required_guards = {"productivity", "effort", "attendance"}
        missing_guards = sorted(guard for guard in required_guards if guard not in prohibited_text)
        if missing_guards:
            risk_flags.append(
                {
                    "code": "missing_non_goal_guard",
                    "message": (
                        "생산성·노력·근태를 추론하지 않는다는 금지 경계를 모두 명시해 주세요. "
                        f"누락: {', '.join(missing_guards)}."
                    ),
                }
            )

    if risk_flags:
        questions.append(
            {
                "id": "risk-review",
                "field": "privacy_boundary",
                "prompt": "이 정책이 사람 감시/인사평가로 사용되지 않는다는 경계와 검토 방법을 명시해 주세요.",
                "required": True,
                "reason": "; ".join(flag["message"] for flag in risk_flags),
            }
        )

    redacted_contract, redactions = redact_value(answers)
    status = "draft_ready" if not questions and not risk_flags else "needs_clarification"
    return {
        "status": status,
        "contract": redacted_contract,
        "questions": questions,
        "risk_flags": risk_flags,
        "redactions": redactions,
        "next_step": "A maintainer must review this contract and compile a versioned policy pack; it is not executable yet.",
        "raw_input_retained": False,
    }
