# Jira dry-run connector

The project models Jira integration without connecting to Jira.

```bash
PYTHONPATH=src python3 -m evidence_workflows.cli dry-run-jira \
  --policy policies/technical-weekly-update.json \
  --input scenarios/cases/P2-busy-senior-engineer.json \
  --issue-key DEMO-1 \
  --operation add_comment
```

The output includes `requires_human_approval: true`, `network_call: false`, and `does_not_infer_duration: true`. It contains only a compact status comment and policy identity; it does not include raw answers or fabricate a time value.

The operation named `draft_worklog` is only a label for an approval plan. This release does not submit a Jira worklog. A real adapter must authenticate outside this package, show the plan to a human, apply it, and read back the remote receipt.
