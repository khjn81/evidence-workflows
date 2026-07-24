from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.redaction import find_sensitive, redact_value  # noqa: E402


class RedactionTests(unittest.TestCase):
    def test_email_and_token_are_replaced_without_returning_matches(self) -> None:
        value = {
            "message": "Contact customer@example.com; token_placeholder_12345678",
            "api_token": "credential_placeholder",
        }
        redacted, findings = redact_value(value)
        serialized = json.dumps(redacted)
        self.assertNotIn("customer@example.com", serialized)
        self.assertNotIn("token_placeholder_12345678", serialized)
        self.assertEqual({item["kind"] for item in findings}, {"email", "token", "sensitive_field"})

    def test_nested_sensitive_scan_contains_only_paths_and_kinds(self) -> None:
        findings = find_sensitive({"nested": ["a@example.com"]})
        self.assertEqual(findings, [{"path": "nested[0]", "kind": "email"}])
