from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.cli import main  # noqa: E402


class CliTests(unittest.TestCase):
    def test_list_policies_prints_all_packs(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["list-policies", "--policies-dir", str(ROOT / "policies")])
        rows = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(len(rows), 4)

    def test_run_scenarios_writes_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "reports"
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "run-scenarios",
                        "--cases-dir",
                        str(ROOT / "scenarios" / "cases"),
                        "--policies-dir",
                        str(ROOT / "policies"),
                        "--output-dir",
                        str(output_dir),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertTrue((output_dir / "evaluation.json").exists())
            self.assertTrue((output_dir / "P4-sensitive-incident-responder.md").exists())

    def test_case_file_can_be_used_as_check_input(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(
                [
                    "check",
                    "--policy",
                    str(ROOT / "policies" / "data-analysis-experiment.json"),
                    "--input",
                    str(ROOT / "scenarios" / "cases" / "P1-careful-data-analyst.json"),
                ]
            )
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "ready")

    def test_scenario_reports_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            for output_dir in (Path(first_dir), Path(second_dir)):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = main(
                        [
                            "run-scenarios",
                            "--cases-dir",
                            str(ROOT / "scenarios" / "cases"),
                            "--policies-dir",
                            str(ROOT / "policies"),
                            "--output-dir",
                            str(output_dir),
                        ]
                    )
                self.assertEqual(code, 0)
            first_files = sorted(path.name for path in Path(first_dir).iterdir())
            second_files = sorted(path.name for path in Path(second_dir).iterdir())
            self.assertEqual(first_files, second_files)
            for name in first_files:
                self.assertEqual(
                    (Path(first_dir) / name).read_bytes(),
                    (Path(second_dir) / name).read_bytes(),
                    name,
                )
