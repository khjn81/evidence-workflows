# Security policy

This project is a local, deterministic prototype. It does not send data to a service or call Jira. The built-in redactor is a safety aid, not a complete data-loss-prevention system.

## Safe use

- Use synthetic or already-sanitized artifacts while evaluating the project.
- Never commit real credentials, customer identifiers, incident logs, or employee records.
- Review the redacted result before copying it into another system.
- Keep raw answers separate from result and audit metadata, with an explicit retention/deletion policy.

## Reporting a vulnerability

Please do not open a public issue containing a secret or personal data. Contact the repository maintainer privately through the security contact configured on GitHub. Include a minimal reproduction with synthetic values whenever possible.
