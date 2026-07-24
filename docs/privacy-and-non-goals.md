# Privacy and non-goals

## Data minimization

The engine returns a redacted artifact and does not retain raw input in the result object. This is a local library behavior, not a complete retention system. A deployment must define where raw answers live, who can read them, how long they remain, and how deletion is handled.

## Prohibited use

Do not use a policy result to rank or discipline a person, infer productivity, estimate attendance, measure effort, detect emotion, or make an employment decision. The policy should evaluate whether an artifact contains enough evidence for a stated coordination decision—not whether its author is a good employee.

## Uncertainty

`unknown` is intentionally visible. For example, “users liked it” without a survey, issue, metric, or other reference cannot become `pass`. A downstream UI must not silently map `unable_to_determine` to a failure score.

## Sensitive data

The v0.1 redactor catches common emails and token-like strings, plus values under common secret-shaped keys. It may miss identifiers or redact too little/too much. Sanitize before entering data and treat the redacted result as a convenience, not a compliance control.
