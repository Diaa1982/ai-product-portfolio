# Strategic Radar — Go-Live Readiness Checklist

**Product ID:** P03  
**Current stage:** Technical deployment candidate  
**Formal go-live ready:** No  
**Permitted data:** Synthetic only

## Implemented in GitHub

- [x] Approved/active/official source checks and domain allowlisting.
- [x] Required source version, timestamps, change summary and SHA-256 evidence reference.
- [x] Six-factor materiality score and null-score analyst routing.
- [x] Fact/interpretation/recommendation separation and advisory disclaimer.
- [x] Human authorization rules for protected outputs.
- [x] PFM taxonomy, dedicated API/UI, synthetic signal and eight tests.
- [x] Hardened container and product/assurance/deployment documentation.

| Gate | Status | Remaining accountable work |
|---|---|---|
| L0 — Strategy and ownership | Partial | Approve sponsor, product owner, outcomes, scope, funding and benefits baseline |
| L1 — Product and process | Technical ready; approval pending | Approve PRD, scanning workflow, delivery formats, exclusions, acceptance and service levels |
| L2 — Data and evidence | Synthetic baseline only | Approve real official sources, owners, rights, domains, quality, lineage, retention and citation rules |
| L3 — AI and knowledge | Deterministic baseline ready | Build/validate ingestion/OCR/classification/recommendation agents; calibrate materiality/confidence and prompt/model controls |
| L4 — Governance and compliance | Partial | Confirm jurisdictions, policy/legal boundaries, decision rights, independent high-impact review and PFM authorities |
| L5 — Security and privacy | Baseline only | Implement SSO/RBAC, egress proxy, SSRF/content-injection controls, encrypted immutable stores and complete security/privacy tests |
| L6 — Architecture and integration | Candidate only | Provision orchestration, workers, database/object/audit stores, source connectors, delivery channels and observability |
| L7 — Verification and assurance | Eight local tests passed | Pass CI/container smoke, corpus precision/recall, citation, security, performance, accessibility and resilience tests |
| L8 — Operating model | Template ready | Name source/product/PFM/analyst/approval/support owners; approve SLO/SLA, RTO/RPO, training and escalation |
| L9 — Deployment and resilience | Container candidate | Validate target CI/CD, signed image, backup/restore, capacity, continuity and rollback exercises |
| L10 — Go-live authority and value | Not started | Complete UAT, accept residual risks and obtain all control/final production approvals |

See [go-live evidence](docs/GO-LIVE-EVIDENCE.md), [PFM alignment](docs/PFM-ALIGNMENT.md), [UAT](docs/UAT.md) and the [portfolio standard](../../docs/GO-LIVE-GATE-STANDARD.md).
