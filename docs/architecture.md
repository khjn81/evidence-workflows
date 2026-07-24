# Architecture

## Runtime boundary

```text
authoring interview
  ↓ safe, complete contract draft
reviewed policy JSON
  ↓ validate + canonicalize + SHA-256
ResolvedPolicyBundle
  ↓ evaluate(artifact)
PolicyResult
  ├── redacted artifact
  ├── CheckResult[]
  ├── InterviewQuestion[]
  └── warnings / redaction metadata
```

The authoring interview accepts a leader/team intake and returns a redacted contract draft. It does not automatically compile or activate a policy. The evaluator accepts a JSON artifact and returns a JSON result. The package has no HTTP client, database client, Jira client, or LLM dependency. This makes the first release easy to audit and replay.

## Why the policy digest matters

Every result carries the policy id, version, and canonical JSON digest. A team can therefore tell which exact criteria produced a result even when the human-readable title is unchanged. Engine version is carried separately because a check implementation can change independently of policy text.

## Check semantics

Checks are intentionally typed. A missing field is `fail`; a present claim without a recognizable reference is `unknown`; an unmet conditional check is `not_applicable`; a value outside an explicit enum is `fail`. Only blocking `fail` and blocking `unknown` affect the top-level status.

The engine does not evaluate arbitrary code from policy files. New check types require implementation, tests, documentation, and a security review of their inference boundary.

## Interview semantics

There are two interview boundaries. The authoring interview asks what a policy is for and what it must not infer. The artifact interview is the question plan returned with a result. A UI or chat adapter can present one question at a time, accept an updated artifact, and rerun the same engine. The engine does not pretend to understand free text beyond conservative reference/date/presence checks.

## Integration boundary

`jira.py` creates a draft plan only. A future adapter must:

1. show the policy and redacted result;
2. obtain explicit human approval;
3. apply the selected mutation with its own credential boundary;
4. read back the remote receipt;
5. store receipt metadata separately from raw answers.
