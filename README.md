# evidence-workflows

Open, deterministic policy interviews for evidence-ready work updates.

`evidence-workflows` turns a team’s explicit working agreement into a small, reviewable policy. A contributor supplies an artifact such as a weekly update, experiment note, incident summary, or presentation brief. The local engine returns checks, follow-up questions, and one of three honest states:

- `ready`: the blocking evidence contract is complete.
- `needs_clarification`: a required field is missing or invalid.
- `unable_to_determine`: a claim exists but cannot be verified from the supplied evidence.

This is deliberately not a productivity tracker, attendance system, or employee scoring tool. It does not infer effort, quality, sentiment, or time spent.

## Why this exists

Jira-like teams often ask for worklogs, but the useful question is usually not “how busy was someone?” It is “what changed, what supports that claim, what is at risk, and what decision or action comes next?” This project makes those criteria visible, versioned, testable, and discussable.

The core loop is:

```text
public policy → contributor answers → deterministic checks → follow-up interview → decision-ready artifact
```

The policy is the team’s contract. The engine is not allowed to invent facts or convert a missing reference into a success score.

The repository also includes a policy-authoring interview. It helps a leader or team turn an implicit standard into a reviewable contract before anyone writes a pack. It never silently compiles that conversation into a deployable policy.

## Quick start

The runtime has no third-party dependency. Python 3.9 or newer is required.

```bash
cd evidence-workflows
PYTHONPATH=src python3 -m evidence_workflows list-policies
PYTHONPATH=src python3 -m evidence_workflows.cli run-scenarios
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Evaluate one artifact:

```bash
PYTHONPATH=src python3 -m evidence_workflows.cli check \
  --policy policies/technical-weekly-update.json \
  --input path/to/artifact.json \
  --format markdown
```

An input can be the artifact object itself or `{ "artifact": { ... } }`. The generated report contains the policy digest, check results, follow-up questions, warnings, and a redacted artifact. Raw input is not retained in the result object.

Start the policy-authoring interview:

```bash
PYTHONPATH=src python3 -m evidence_workflows.cli author-interview
PYTHONPATH=src python3 -m evidence_workflows.cli author-interview \
  --input scenarios/policy-authoring/leader-intake.json
```

The first command prints the questions. The second evaluates a synthetic leader intake and returns a policy contract draft. A maintainer still needs to review and translate it into a versioned policy pack.

Run the five synthetic personas:

```bash
PYTHONPATH=src python3 evals/evaluate_scenarios.py
```

The committed examples live in [`scenarios/cases`](scenarios/cases), and generated reports live in [`scenarios/outputs`](scenarios/outputs). The five cases intentionally include a complete analyst, a terse senior engineer, an optimistic manager with an unverifiable claim, an incident responder who pasted sensitive data, and a junior researcher whose experiment is still in progress.

## Policy packs

| Pack | Purpose | Important boundary |
|---|---|---|
| [`technical-weekly-update.json`](policies/technical-weekly-update.json) | State, evidence, impact/risk, next action | Does not ask for hours or attendance |
| [`data-analysis-experiment.json`](policies/data-analysis-experiment.json) | Question, hypothesis, method, evidence, next experiment | An `in_progress` experiment does not need a final result |
| [`incident-investigation.json`](policies/incident-investigation.json) | Impact, evidence, mitigation, safety action | Sensitive patterns block the artifact and are redacted in output |
| [`presentation-brief.json`](policies/presentation-brief.json) | Decision, audience, claims, evidence, ask | Unverifiable claims remain `unknown` |

Policy JSON is intentionally small. v0.1 supports only typed checks (`present`, `evidence_reference`, `date_reference`, `conditional_present`, `allowed_value`, and `no_sensitive_data`). It does not execute arbitrary expressions.

Read [`docs/policy-authoring.md`](docs/policy-authoring.md) before adding a pack. In particular, every pack must document its purpose, non-goals, minimum evidence, uncertainty behavior, privacy boundary, owner, and positive/negative fixtures.

## Jira-shaped integration

The CLI can create a no-network, approval-gated plan:

```bash
PYTHONPATH=src python3 -m evidence_workflows.cli dry-run-jira \
  --policy policies/technical-weekly-update.json \
  --input scenarios/cases/P2-busy-senior-engineer.json \
  --issue-key DEMO-1 \
  --operation add_comment
```

This package does not call Jira, infer a duration, submit a worklog, or store credentials. A future connector must review the plan, apply it with its own authenticated client, and read back a receipt. Jira’s official REST worklog surface is documented [here](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/); Forge issue panels and workflow validators are documented [here](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-panel/) and [here](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-workflow-validator/).

## Safety and non-goals

Do not use this project to rank people, infer work ethic, estimate attendance, or automatically make employment decisions. Policies must be visible to the people answering them. “Unknown” is a valid output, not a hidden penalty. See [`docs/privacy-and-non-goals.md`](docs/privacy-and-non-goals.md) and [`SECURITY.md`](SECURITY.md).

The built-in redactor catches common email and token patterns as a local safety net. It is not a complete DLP system. Sensitive data should be removed before input, and reports should be reviewed before they leave the local environment.

## Project map

```text
src/evidence_workflows/  policy loader, evaluator, redaction, CLI, dry-run connector
policies/                 versioned policy packs
scenarios/                synthetic inputs and generated reports
evals/                    evaluator-quality rubric and runner
tests/                    unit, integration, and scenario regression tests
docs/                     architecture, authoring, privacy, connector guidance
```

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m evidence_workflows.cli run-scenarios --output-dir /tmp/evidence-workflows-results
git diff --check
```

The project uses the MIT license. Contributions that add a policy pack should include synthetic positive and negative cases and must not introduce personal-performance scoring or hidden criteria. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
