"""Conservative local redaction for reports and dry-run payloads."""

from __future__ import annotations

import re
from typing import Any


_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "email",
        re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])"),
        "<redacted:email>",
    ),
    (
        "token",
        re.compile(r"\b(?:sk|ghp|xoxb|xoxp|ATATT)[-_][A-Za-z0-9_-]{8,}\b"),
        "<redacted:token>",
    ),
    (
        "token",
        re.compile(r"\b(?:token|secret)[-_](?:placeholder|fake)[-_A-Za-z0-9]{8,}\b", re.I),
        "<redacted:token>",
    ),
)
_SENSITIVE_KEY = re.compile(r"(?:password|passwd|secret|token|api[_-]?key|authorization)", re.I)


def _string_findings(text: str, path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for kind, pattern, _replacement in _PATTERNS:
        if pattern.search(text):
            findings.append({"path": path or "$", "kind": kind})
    return findings


def find_sensitive(value: Any, path: str = "") -> list[dict[str, str]]:
    """Return only safe metadata about sensitive values; never return matches."""

    findings: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if _SENSITIVE_KEY.search(str(key)) and child not in (None, "", [], {}):
                findings.append({"path": child_path, "kind": "sensitive_field"})
                continue
            findings.extend(find_sensitive(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_sensitive(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        findings.extend(_string_findings(value, path))
    return findings


def redact_text(text: str, path: str = "") -> tuple[str, list[dict[str, str]]]:
    redacted = text
    findings: list[dict[str, str]] = []
    for kind, pattern, replacement in _PATTERNS:
        if pattern.search(redacted):
            findings.append({"path": path or "$", "kind": kind})
            redacted = pattern.sub(replacement, redacted)
    return redacted, findings


def redact_value(value: Any, path: str = "") -> tuple[Any, list[dict[str, str]]]:
    """Redact common credentials and direct identifiers recursively."""

    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        findings: list[dict[str, str]] = []
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if _SENSITIVE_KEY.search(str(key)) and child not in (None, "", [], {}):
                redacted[key] = "<redacted:sensitive_field>"
                findings.append({"path": child_path, "kind": "sensitive_field"})
                continue
            child_redacted, child_findings = redact_value(child, child_path)
            redacted[key] = child_redacted
            findings.extend(child_findings)
        return redacted, findings
    if isinstance(value, list):
        redacted_items: list[Any] = []
        findings = []
        for index, child in enumerate(value):
            child_redacted, child_findings = redact_value(child, f"{path}[{index}]")
            redacted_items.append(child_redacted)
            findings.extend(child_findings)
        return redacted_items, findings
    if isinstance(value, str):
        return redact_text(value, path)
    return value, []
