# Security and Privacy

## Baseline controls in code

- Typed input validation, bounded scores and allow-listed assessment modes/classes.
- No external AI/model call in deterministic baseline.
- Synthetic-data warning and no embedded secrets.
- Explicit human approval boundary and fail-safe routing for incomplete/high-risk cases.
- Non-root container process and health check.

## Production controls required

Enterprise SSO/OIDC; server-side RBAC and segregation of duties; TLS; encrypted database and backups; managed secrets; WAF/rate limiting; immutable audit trail; security logging and alerts; dependency/container scanning; vulnerability and penetration tests; privacy impact assessment; field minimization; approved retention/deletion; breach and incident procedures.

## Key threats

Role spoofing, evidence tampering, configuration manipulation, sensitive-data disclosure, injection in free text, denial of service and audit loss. Production mitigations must bind roles to signed claims, hash/version evidence and config, sanitize rendering, enforce limits, and fail closed when audit or identity services fail.

## Prohibited production use until approval

Do not store personal, confidential or restricted content; connect organizational systems; represent a score as approval; or allow automated consequential decisions until the accountable security, privacy, legal, data and AI-governance authorities sign the evidence pack.
