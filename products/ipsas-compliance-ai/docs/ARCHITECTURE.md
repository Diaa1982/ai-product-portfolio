# Architecture

## Layers

1. **Controlled intake:** manual PDF/Excel or structured API in the MVP; later owner-approved ledger, reconciliation, reporting, SharePoint or email adapters.
2. **Extraction and evidence:** structured accounting fields, source references, document versions and evidence-strength classification.
3. **Controlled knowledge:** organization-approved policies, templates and applicable requirement references, versioned and effective-dated.
4. **Deterministic checks:** balance, cut-off, approval, SoD, reconciliation, aging, disclosure and comparative checks.
5. **Assisted analysis:** future evidence comparison/classification and draft recommendations with confidence and citations.
6. **Human workflow:** accounting-manager or equivalent review, return, approval/rejection reference and escalation.
7. **Assurance:** immutable audit/evidence, evaluations, monitoring, versioning, incident response and rollback.

The repository implements structured intake, deterministic checks, a human-review contract and user interface over synthetic data. It does not include live integrations, document extraction, authoritative IPSAS content or a production approval queue.
