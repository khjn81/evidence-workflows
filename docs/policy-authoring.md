# Policy authoring guide

A good policy is a small public contract, not a manager’s hidden checklist.

## Executable authoring interview

Use the local authoring interview before adding or changing a policy pack:

```bash
PYTHONPATH=src python3 -m evidence_workflows.cli author-interview
PYTHONPATH=src python3 -m evidence_workflows.cli author-interview \
  --input scenarios/policy-authoring/leader-intake.json
```

It collects the decision, minimum evidence, allowed lifecycle states, unknown behavior, privacy boundary, prohibited inferences, action boundary, owner, and review date. A complete and safe intake returns `draft_ready`; missing fields or risky intent returns `needs_clarification`. It produces a reviewable contract, not an automatically deployable policy.

## Required design questions

Before writing JSON, answer:

1. What decision or coordination problem does this artifact support?
2. What is the minimum evidence needed to support that decision?
3. Which states are allowed while work is incomplete or blocked?
4. What can the policy not infer?
5. Which fields may contain personal or credential data, and how are they removed?
6. Who owns the policy and when will it expire or be reviewed?

## Field and question rules

- Ask for outcomes, evidence, impact/risk, and next action.
- Give each required field one answerable prompt.
- Use nested fields for structured ownership and due dates rather than parsing a long paragraph.
- Keep optional safety questions non-required; trigger them only when a safety check fails.
- Do not ask how many hours someone worked unless a separate, explicit operational accounting requirement exists outside this project.

## Check rules

- Use `present` for a genuinely required value.
- Use `evidence_reference` when a claim must point to a URL, Jira key, PR, or commit.
- Use `date_reference` for a follow-up date.
- Use `conditional_present` to model lifecycle states such as `in_progress` versus `completed`.
- Use `allowed_value` when a lifecycle field must be one of an explicit set.
- Use `no_sensitive_data` as a safety gate, not as a quality score.
- Mark a check blocking only when the downstream decision cannot proceed safely without it.

## Review checklist

- Does the policy state its non-goals and prohibited inferences?
- Can a contributor answer each question without guessing what the leader “really means”?
- Does missing evidence produce a useful question rather than a person score?
- Does an unverifiable claim remain `unknown`?
- Does unfinished work have an explicit valid state?
- Are positive, missing-field, unverifiable, and sensitive-data fixtures included?
