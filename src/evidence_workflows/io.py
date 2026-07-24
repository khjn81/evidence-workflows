"""JSON and Markdown I/O for reproducible local reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    json_path = Path(path)
    try:
        return json.loads(json_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"JSON file not found: {json_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {json_path}: {exc.msg}") from exc


def write_json(path: str | Path, value: Any) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(result: dict[str, Any], evaluation: dict[str, Any] | None = None) -> str:
    lines = [
        f"# Evidence workflow result: `{result['policy_id']}`",
        "",
        f"- Status: **{result['status']}**",
        f"- Policy version: `{result['policy_version']}`",
        f"- Policy digest: `{result['policy_digest']}`",
        f"- Engine version: `{result['engine_version']}`",
        "",
        "## Artifact (redacted)",
        "",
        "```json",
        json.dumps(result["artifact"], ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Checks",
        "",
        "| Check | Status | Blocking | Message |",
        "|---|---|---:|---|",
    ]
    for check in result["checks"]:
        lines.append(
            f"| `{_cell(check['id'])}` | `{_cell(check['status'])}` | "
            f"{_cell(check['blocking'])} | {_cell(check['message'])} |"
        )
    lines.extend(["", "## Follow-up questions", ""])
    if result["questions"]:
        for question in result["questions"]:
            lines.append(f"- **{question['field']}** — {question['prompt']} ({question['reason']})")
    else:
        lines.append("No follow-up questions.")
    lines.extend(["", "## Warnings", ""])
    if result["warnings"]:
        lines.extend(f"- {warning}" for warning in result["warnings"])
    else:
        lines.append("No warnings.")
    if result["redactions"]:
        lines.extend(
            [
                "",
                "## Redactions",
                "",
                f"{len(result['redactions'])} sensitive pattern(s) were redacted from the report.",
            ]
        )
    if evaluation is not None:
        lines.extend(
            [
                "",
                "## Synthetic evaluation",
                "",
                f"- Score: **{evaluation['score']} / 100**",
                f"- Overall: **{'pass' if evaluation['overall_pass'] else 'review'}**",
            ]
        )
        for name, criterion in evaluation["criteria"].items():
            lines.append(f"- `{name}`: {'pass' if criterion['passed'] else 'fail'} — {criterion['note']}")
    return "\n".join(lines) + "\n"
