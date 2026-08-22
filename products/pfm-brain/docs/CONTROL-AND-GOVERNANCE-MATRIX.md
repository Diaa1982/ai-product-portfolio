# Control and Governance Matrix

| Risk | Embedded MVP control | Required production ownership/evidence |
|---|---|---|
| Invalid master or transaction reference | Master-data prerequisites and required IDs | Data owners; reference-integrity and load reports |
| Incorrect fiscal period/currency | FY2026/AED controlled baseline | Accounting/budget owner-approved calendar and currency rules |
| Duplicate or unsupported record | Duplicate flag and evidence requirement | Source reconciliation and evidence-store control |
| Calculation error | Deterministic formulas, versioned config and tests | Independent reconciliation and formula approval |
| Report inconsistency | Expected-result reconciliation at AED 0.01 | Signed report-to-source reconciliation |
| SoD conflict | Requester cannot equal approver | IAM/delegation integration and periodic access review |
| Authority breach | Maximum-amount comparison and escalation | Effective-dated authority matrix and authorized decision record |
| Protected/critical action | Human-approval interruption | Applicable legal/policy delegation and approval system of record |
| Unsupported narrative | Facts/calculations/assumptions/risks separated | Reviewer confirmation, citation and evaluation record |
| Configuration/model change | Versioned files, tests and CI | Change advisory, independent assurance and rollback evidence |
| Audit/privacy/security failure | Digest and documented controls | Tamper-evident logs, retention, privacy/security approval |

No amount comparison constitutes an approval. Authority depends on applicable law, policy, organizational delegation, transaction type and effective dates, none of which may be assumed from this generic configuration.
