"""Reproducible entry point for the five synthetic persona evaluation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from evidence_workflows.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(
        main(
            [
                "run-scenarios",
                "--cases-dir",
                str(ROOT / "scenarios" / "cases"),
                "--policies-dir",
                str(ROOT / "policies"),
                "--output-dir",
                str(ROOT / "scenarios" / "outputs"),
            ]
        )
    )
