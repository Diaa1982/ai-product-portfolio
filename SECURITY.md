# Security Policy

## Baseline controls

- Never commit secrets or production data.
- Use environment variables and approved secret stores.
- Apply least privilege and role-based access.
- Separate development, test, pilot and production environments.
- Record security-relevant and approval events in tamper-evident logs.
- Validate uploaded files, content types, size and malware status.
- Defend retrieval and agent workflows against prompt injection and untrusted instructions.
- Redact sensitive data from prompts, logs and model responses.
- Require human approval for consequential financial, legal, audit, risk and control actions.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Do not open public issues containing exploit details, credentials, confidential documents or personal data.

## Production gate

No package is production-ready until threat modelling, dependency review, SAST, secret scanning, access-control testing, data-protection review, model red-teaming, incident response and recovery tests are completed.
