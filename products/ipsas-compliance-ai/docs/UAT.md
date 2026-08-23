# User Acceptance Testing

Use synthetic or formally approved masked records.

| Scenario | Expected result |
|---|---|
| Balanced, supported, approved journal | Review ready; no configured exception; no formal compliance conclusion |
| Unbalanced/invalid account/missing support | High-severity potential exception and human review |
| Outside period or same preparer/approver | Cut-off or SoD exception |
| Low confidence/missing evidence or references | `INSUFFICIENT_INFORMATION` |
| Reconciliation difference/aged or unsupported item | Difference, aging and evidence exception list |
| Missing/partial disclosure or comparative | Draft gap checklist and review route |
| Reporting-impact/material case | Accounting-manager or equivalent human gate |
| Post/approve/close/certify/publish action | Autonomous execution denied |

Sign-off requires accounting policy/reporting owners, reconciliation/journal process owners, data owner, technology, security/privacy, internal control and applicable assurance stakeholders. UAT does not constitute an accounting or audit opinion.
