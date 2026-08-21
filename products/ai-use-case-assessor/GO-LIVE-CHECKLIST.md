# AI Use Case Assessor — Go-Live Readiness Checklist

**Product ID:** P08  
**Current stage:** Technical deployment candidate  
**Formal go-live ready:** No  
**Permitted data:** Synthetic only

## Implemented in GitHub

- [x] Versioned criteria, 60/40 weighted scoring, risk tiers and four portfolio classes.
- [x] Client-led, diagnostic-led and hybrid intake model.
- [x] Incomplete-information and high-risk safeguards.
- [x] Dedicated API, web interface, synthetic example and automated tests.
- [x] CEO-only protected final-approval rule in application logic.
- [x] Non-root container, health check, deployment/rollback guide and operations runbook.
- [x] PRD, architecture, data, scoring, API, security/privacy, test, UAT and evidence documents.

## Gate assessment

| Gate | Status | Remaining accountable work |
|---|---|---|
| L0 — Strategy and ownership | Partial | Name sponsor/product owner; approve business case, funding, outcomes and benefits baseline |
| L1 — Product and process | Technical ready; approval pending | Approve PRD, target process, exclusions, acceptance criteria and service levels |
| L2 — Data and evidence | Blocked for production | Approve real sources/owners, field collection, quality, classification, lineage, retention and lawful use |
| L3 — AI and knowledge | Technical ready; calibration pending | Approve config; run inter-rater reliability, sensitivity, edge-case and impact validation |
| L4 — Governance and compliance | Partial | Map policy/legal obligations, risk tier, segregation and independent high-impact assurance |
| L5 — Security and privacy | Baseline only | Implement enterprise IAM/RBAC, encrypted persistence/secrets/audit; pass privacy, vulnerability and penetration reviews |
| L6 — Architecture and integration | Candidate only | Provision target environments, identity, database, approved connectors and observability |
| L7 — Verification and assurance | Automated baseline passed locally | Pass CI, security, performance, accessibility, resilience and representative-corpus testing |
| L8 — Operating model | Template ready | Name support/control owners; approve RACI, SLA/SLO, RTO/RPO, training and change procedures |
| L9 — Deployment and resilience | Container candidate | Validate target CI/CD, signed image, backup/restore, rollback, capacity and continuity exercises |
| L10 — Go-live authority and value | Not started | Complete UAT, accept residual risk, obtain all control approvals and record CEO go-live decision |

## Mandatory release evidence

- [ ] Approved product/business case and configuration version.
- [ ] Production data, identity, integration and infrastructure approvals.
- [ ] Security/privacy/legal/responsible-AI assessment and closed critical findings.
- [ ] Representative-corpus validation, non-functional test summary and business UAT sign-off.
- [ ] Named operating/support model and successful recovery exercise.
- [ ] Residual-risk register and CEO final go-live approval.

See the [evidence index](docs/GO-LIVE-EVIDENCE.md), [UAT pack](docs/UAT.md) and [portfolio go-live standard](../../docs/GO-LIVE-GATE-STANDARD.md).
