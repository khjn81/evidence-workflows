"""Policy loading, validation, and stable bundle identity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import __version__
from .models import ResolvedPolicyBundle

API_VERSION = "evidence-workflows/v1"
ALLOWED_CHECK_TYPES = {
    "present",
    "evidence_reference",
    "date_reference",
    "conditional_present",
    "no_sensitive_data",
    "allowed_value",
}


class PolicyError(ValueError):
    """Raised when a policy cannot be safely resolved."""


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PolicyError(f"{label} must be a non-empty string")
    return value


def _validate_condition(condition: Any, label: str) -> None:
    if not isinstance(condition, dict):
        raise PolicyError(f"{label} must be an object")
    _require_string(condition.get("field"), f"{label}.field")
    operators = [key for key in ("equals", "in") if key in condition]
    if len(operators) != 1:
        raise PolicyError(f"{label} must contain exactly one of equals or in")
    if "in" in condition and (
        not isinstance(condition["in"], list) or not condition["in"]
    ):
        raise PolicyError(f"{label}.in must be a non-empty list")


def validate_policy(policy: dict[str, Any], source: str = "policy") -> None:
    """Validate the deliberately small v1 policy contract."""

    if not isinstance(policy, dict):
        raise PolicyError(f"{source} must contain a JSON object")
    if policy.get("api_version") != API_VERSION:
        raise PolicyError(f"{source}.api_version must be {API_VERSION!r}")
    if policy.get("kind") != "Policy":
        raise PolicyError(f"{source}.kind must be 'Policy'")

    metadata = policy.get("metadata")
    if not isinstance(metadata, dict):
        raise PolicyError(f"{source}.metadata must be an object")
    _require_string(metadata.get("id"), f"{source}.metadata.id")
    _require_string(metadata.get("version"), f"{source}.metadata.version")
    _require_string(metadata.get("title"), f"{source}.metadata.title")

    spec = policy.get("spec")
    if not isinstance(spec, dict):
        raise PolicyError(f"{source}.spec must be an object")
    _require_string(spec.get("purpose"), f"{source}.spec.purpose")
    _require_string(spec.get("artifact_type"), f"{source}.spec.artifact_type")

    required_fields = spec.get("required_fields", [])
    if not isinstance(required_fields, list) or not all(
        isinstance(item, str) and item.strip() for item in required_fields
    ):
        raise PolicyError(f"{source}.spec.required_fields must be a list of strings")

    questions = spec.get("questions")
    if not isinstance(questions, list) or not questions:
        raise PolicyError(f"{source}.spec.questions must be a non-empty list")
    question_ids: set[str] = set()
    for index, question in enumerate(questions):
        label = f"{source}.spec.questions[{index}]"
        if not isinstance(question, dict):
            raise PolicyError(f"{label} must be an object")
        question_id = _require_string(question.get("id"), f"{label}.id")
        if question_id in question_ids:
            raise PolicyError(f"duplicate question id: {question_id}")
        question_ids.add(question_id)
        _require_string(question.get("field"), f"{label}.field")
        _require_string(question.get("prompt"), f"{label}.prompt")
        if not isinstance(question.get("required"), bool):
            raise PolicyError(f"{label}.required must be boolean")
        if "when" in question:
            _validate_condition(question["when"], f"{label}.when")

    checks = spec.get("checks")
    if not isinstance(checks, list) or not checks:
        raise PolicyError(f"{source}.spec.checks must be a non-empty list")
    check_ids: set[str] = set()
    for index, check in enumerate(checks):
        label = f"{source}.spec.checks[{index}]"
        if not isinstance(check, dict):
            raise PolicyError(f"{label} must be an object")
        check_id = _require_string(check.get("id"), f"{label}.id")
        if check_id in check_ids:
            raise PolicyError(f"duplicate check id: {check_id}")
        check_ids.add(check_id)
        check_type = _require_string(check.get("type"), f"{label}.type")
        if check_type not in ALLOWED_CHECK_TYPES:
            allowed = ", ".join(sorted(ALLOWED_CHECK_TYPES))
            raise PolicyError(f"{label}.type {check_type!r} is not supported; use {allowed}")
        _require_string(check.get("field"), f"{label}.field")
        _require_string(check.get("message"), f"{label}.message")
        if check_type == "allowed_value":
            values = check.get("values")
            if not isinstance(values, list) or not values:
                raise PolicyError(f"{label}.values must be a non-empty list for allowed_value")
        if not isinstance(check.get("blocking"), bool):
            raise PolicyError(f"{label}.blocking must be boolean")
        severity = check.get("severity", "error" if check["blocking"] else "warning")
        if severity not in {"error", "warning", "info"}:
            raise PolicyError(f"{label}.severity must be error, warning, or info")
        if "question_id" in check and check["question_id"] not in question_ids:
            raise PolicyError(f"{label}.question_id does not reference a known question")
        if "when" in check:
            _validate_condition(check["when"], f"{label}.when")

    progress_warning = spec.get("progress_warning")
    if progress_warning is not None:
        if not isinstance(progress_warning, dict):
            raise PolicyError(f"{source}.spec.progress_warning must be an object")
        _require_string(progress_warning.get("field"), f"{source}.spec.progress_warning.field")
        _require_string(progress_warning.get("message"), f"{source}.spec.progress_warning.message")
        values = progress_warning.get("values")
        if not isinstance(values, list) or not values:
            raise PolicyError(f"{source}.spec.progress_warning.values must be a non-empty list")

    prohibited = spec.get("prohibited_inferences", [])
    if not isinstance(prohibited, list) or not all(isinstance(item, str) for item in prohibited):
        raise PolicyError(f"{source}.spec.prohibited_inferences must be a list of strings")


def load_policy(path: str | Path) -> dict[str, Any]:
    policy_path = Path(path)
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PolicyError(f"policy file not found: {policy_path}") from exc
    except json.JSONDecodeError as exc:
        raise PolicyError(f"invalid JSON in {policy_path}: {exc.msg}") from exc
    validate_policy(policy, str(policy_path))
    return policy


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_policy(path: str | Path) -> ResolvedPolicyBundle:
    policy_path = Path(path)
    policy = load_policy(policy_path)
    digest = hashlib.sha256(canonical_json(policy).encode("utf-8")).hexdigest()
    return ResolvedPolicyBundle(
        policy=policy,
        policy_path=str(policy_path),
        digest=digest,
        engine_version=__version__,
    )
