"""Command-line interface for local policy interviews and evaluations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .authoring import evaluate_authoring
from .engine import evaluate
from .evaluation import assess_case
from .io import load_json, render_markdown, write_json
from .jira import build_dry_run_plan
from .policy import PolicyError, resolve_policy


def _policy_path(policies_dir: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    candidate = policies_dir / value
    if candidate.suffix != ".json":
        candidate = candidate.with_suffix(".json")
    return candidate


def _artifact_from_input(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and "artifact" in value and isinstance(value["artifact"], dict):
        value = value["artifact"]
    if not isinstance(value, dict):
        raise ValueError("input must be an artifact object or {\"artifact\": {...}}")
    return value


def _evaluate_one(policy_path: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    bundle = resolve_policy(policy_path)
    return evaluate(bundle, artifact).to_dict()


def _cmd_list_policies(args: argparse.Namespace) -> int:
    policies_dir = Path(args.policies_dir)
    rows = []
    for path in sorted(policies_dir.glob("*.json")):
        bundle = resolve_policy(path)
        rows.append(
            {
                "id": bundle.metadata["id"],
                "version": bundle.metadata["version"],
                "title": bundle.metadata["title"],
                "file": str(path),
                "digest": bundle.digest,
            }
        )
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    result = _evaluate_one(Path(args.policy), _artifact_from_input(load_json(args.input)))
    if args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _cmd_author_interview(args: argparse.Namespace) -> int:
    answers: Any = {} if not args.input else load_json(args.input)
    if isinstance(answers, dict) and isinstance(answers.get("answers"), dict):
        answers = answers["answers"]
    result = evaluate_authoring(answers)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _write_case_outputs(output_dir: Path, case: dict[str, Any], result: dict[str, Any], evaluation: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = case["id"]
    write_json(output_dir / f"{stem}.json", {"case": {"id": case["id"], "persona": case["persona"]}, "result": result, "evaluation": evaluation})
    (output_dir / f"{stem}.md").write_text(
        render_markdown(result, evaluation),
        encoding="utf-8",
    )


def _render_evaluation_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Synthetic persona evaluation",
        "",
        "This report evaluates the evaluator on synthetic personas. It is not an employee-performance assessment.",
        "",
        f"- Cases: **{summary['case_count']}**",
        f"- Passed: **{summary['passed_count']} / {summary['case_count']}**",
        f"- Average score: **{summary['average_score']} / 100**",
        "",
        "| Case | Persona | Expected | Actual | Score | Overall |",
        "|---|---|---|---|---:|---|",
    ]
    for item in summary["cases"]:
        lines.append(
            f"| `{item['case_id']}` | {item['persona']} | `{item['expected_status']}` | "
            f"`{item['actual_status']}` | {item['score']} | "
            f"{'pass' if item['overall_pass'] else 'review'} |"
        )
    lines.extend(["", "## Interpretation", ""])
    lines.extend(f"- {note}" for note in summary["interpretation"])
    return "\n".join(lines) + "\n"


def _cmd_run_scenarios(args: argparse.Namespace) -> int:
    cases_dir = Path(args.cases_dir)
    policies_dir = Path(args.policies_dir)
    output_dir = Path(args.output_dir)
    evaluations: list[dict[str, Any]] = []
    for case_path in sorted(cases_dir.glob("*.json")):
        case = load_json(case_path)
        if not isinstance(case, dict):
            raise ValueError(f"scenario must be an object: {case_path}")
        policy_path = _policy_path(policies_dir, case["policy"])
        result = _evaluate_one(policy_path, _artifact_from_input(case["artifact"]))
        evaluation = assess_case(case, result)
        _write_case_outputs(output_dir, case, result, evaluation)
        evaluations.append(evaluation)

    if not evaluations:
        raise ValueError(f"no scenario JSON files found in {cases_dir}")
    average_score = round(sum(item["score"] for item in evaluations) / len(evaluations), 2)
    summary = {
        "case_count": len(evaluations),
        "passed_count": sum(1 for item in evaluations if item["overall_pass"]),
        "average_score": average_score,
        "cases": evaluations,
        "interpretation": [
            "A pass means the deterministic engine met the synthetic case contract; it does not validate organizational usefulness.",
            "A ready result still requires a human to decide whether the artifact belongs in the target workflow.",
            "unknown is intentionally preserved when a claim lacks a verifiable reference.",
        ],
    }
    write_json(output_dir / "evaluation.json", summary)
    (output_dir / "evaluation.md").write_text(_render_evaluation_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["passed_count"] == summary["case_count"] else 1


def _cmd_dry_run_jira(args: argparse.Namespace) -> int:
    bundle = resolve_policy(args.policy)
    artifact = _artifact_from_input(load_json(args.input))
    plan = build_dry_run_plan(evaluate(bundle, artifact), args.issue_key, args.operation)
    if args.output:
        write_json(args.output, plan)
    print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run public, deterministic evidence policies locally.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-policies", help="list validated policy packs")
    list_parser.add_argument("--policies-dir", default="policies")
    list_parser.set_defaults(handler=_cmd_list_policies)

    check_parser = subparsers.add_parser("check", help="evaluate one artifact")
    check_parser.add_argument("--policy", required=True)
    check_parser.add_argument("--input", required=True)
    check_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    check_parser.set_defaults(handler=_cmd_check)

    author_parser = subparsers.add_parser("author-interview", help="interview a leader before authoring a policy pack")
    author_parser.add_argument("--input", help="JSON file containing authoring answers")
    author_parser.set_defaults(handler=_cmd_author_interview)

    scenario_parser = subparsers.add_parser("run-scenarios", help="run all synthetic persona cases")
    scenario_parser.add_argument("--cases-dir", default="scenarios/cases")
    scenario_parser.add_argument("--policies-dir", default="policies")
    scenario_parser.add_argument("--output-dir", default="scenarios/outputs")
    scenario_parser.set_defaults(handler=_cmd_run_scenarios)

    jira_parser = subparsers.add_parser("dry-run-jira", help="create an approval-gated, no-network Jira plan")
    jira_parser.add_argument("--policy", required=True)
    jira_parser.add_argument("--input", required=True)
    jira_parser.add_argument("--issue-key", required=True)
    jira_parser.add_argument("--operation", choices=("add_comment", "draft_worklog"), default="add_comment")
    jira_parser.add_argument("--output")
    jira_parser.set_defaults(handler=_cmd_dry_run_jira)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except (PolicyError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
