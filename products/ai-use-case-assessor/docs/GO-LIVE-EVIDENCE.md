# Go-Live Evidence and Decision Record

## Current decision

**Technical deployment candidate:** Yes; repository CI, container build and live health/UI/API smoke test passed.  
**Approved for organizational production:** No.  
**Permitted data now:** Synthetic only.

## Evidence available in GitHub

| Evidence | Location | Position |
|---|---|---|
| Product scope and acceptance | [PRD](PRD.md) | Documented |
| Architecture and trust boundaries | [Architecture](ARCHITECTURE.md) | Candidate documented; target approval pending |
| Versioned scoring rules | [Configuration](../config/scoring.v1.json) and [method](SCORING-METHODOLOGY.md) | Implemented; governance calibration pending |
| API and interface | `/p08`, `/p08/*`, [API](API.md) | Implemented |
| Security/privacy control plan | [Security and privacy](SECURITY-PRIVACY.md) | Baseline documented; target testing pending |
| Container and rollback | [Deployment](DEPLOYMENT.md) | Implemented candidate; target infrastructure pending |
| Automated tests | `tests/test_p08_assessor.py` and CI | Implemented; Portfolio Quality run 46 passed, including image build and live API smoke test |
| Business acceptance | [UAT pack](UAT.md) | Pending |
| Operations | [Runbook](RUNBOOK.md) | Template ready; named owners/SLO/RTO/RPO pending |
| L0–L10 decision | [Checklist](../GO-LIVE-CHECKLIST.md) | Not approved |

## Approval record

| Authority | Decision | Name/date/reference |
|---|---|---|
| Product/business owner | Pending | — |
| Data owner | Pending | — |
| Security and privacy | Pending | — |
| Legal/compliance/AI governance | Pending | — |
| Platform/operations | Pending | — |
| Business UAT owner | Pending | — |
| CEO final go-live authority | Pending | — |

This page must not be changed to “production approved” until every mandatory gate has evidence, residual risks are accepted by accountable roles and the CEO decision is recorded.
