# P11 — IPSAS Compliance AI

IPSAS Compliance AI is an evidence-led accounting quality and reporting exception-review product. It supports journal quality review, reconciliation exception tracking and disclosure checklist review against organization-approved policy and cited requirement references.

**Status:** technical deployment candidate; synthetic-only; no formal IPSAS compliance determination; not approved for production or external reporting.

## Implemented MVP

- Journal balance, account, support, workflow approval, segregation-of-duties, period cut-off and materiality checks.
- Ledger/external balance reconciliation, unreconciled-item evidence and aging checks.
- Disclosure completeness, evidence/policy reference and comparative-information checks.
- Evidence strength and low-confidence `INSUFFICIENT_INFORMATION` routing.
- Material/reporting-impact human review gate.
- Separate facts, calculations, potential exceptions, assumptions, recommendations, evidence and audit digest.
- Denial of autonomous accounting approval, posting, period close, certification and publication actions.
- API and Accounting Review Workbench at `/p11`.

## Run

```bash
docker compose -f products/ipsas-compliance-ai/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p11`.

## Documentation

- [Product requirements](docs/PRD.md) and [architecture](docs/ARCHITECTURE.md)
- [Accounting review methodology](docs/ACCOUNTING-REVIEW-METHODOLOGY.md)
- [Controlled knowledge standard](docs/CONTROLLED-KNOWLEDGE-STANDARD.md)
- [Journal, reconciliation and disclosure controls](docs/REVIEW-CONTROLS.md)
- [Governance matrix](docs/CONTROL-RISK-GOVERNANCE-MATRIX.md)
- [API](docs/API.md), [data model](docs/DATA-MODEL.md), [security](docs/SECURITY-PRIVACY.md)
- [Deployment](docs/DEPLOYMENT.md), [runbook](docs/RUNBOOK.md), [test plan](docs/TEST-PLAN.md), [UAT](docs/UAT.md)
- [Roadmap](docs/ROADMAP.md), [go-live evidence](docs/GO-LIVE-EVIDENCE.md), [checklist](GO-LIVE-CHECKLIST.md)

## Professional judgement boundary

“No exception identified” means only that configured checks found no issue in the supplied evidence. It is not a compliance opinion. Qualified accounting officials retain responsibility for the applicable accounting framework, accounting treatment, materiality, correction, journal approval, close, certification, financial statements and external publication.
