from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.policy import PolicyError, resolve_policy, validate_policy  # noqa: E402


class PolicyTests(unittest.TestCase):
    def test_all_policy_packs_resolve(self) -> None:
        paths = sorted((ROOT / "policies").glob("*.json"))
        self.assertEqual(len(paths), 4)
        for path in paths:
            bundle = resolve_policy(path)
            self.assertEqual(len(bundle.digest), 64)
            self.assertTrue(bundle.metadata["id"])

    def test_digest_is_stable_for_same_policy(self) -> None:
        path = ROOT / "policies" / "data-analysis-experiment.json"
        self.assertEqual(resolve_policy(path).digest, resolve_policy(path).digest)

    def test_unknown_check_type_is_rejected(self) -> None:
        policy = json.loads((ROOT / "policies" / "presentation-brief.json").read_text())
        invalid = copy.deepcopy(policy)
        invalid["spec"]["checks"][0]["type"] = "guess_quality"
        with self.assertRaises(PolicyError):
            validate_policy(invalid, "fixture")

    def test_allowed_value_requires_values(self) -> None:
        policy = json.loads((ROOT / "policies" / "data-analysis-experiment.json").read_text())
        invalid = copy.deepcopy(policy)
        invalid["spec"]["checks"][1].pop("values")
        with self.assertRaises(PolicyError):
            validate_policy(invalid, "fixture")
