# Signal Detection Agent — Go-Live Readiness Checklist

**Product ID:** P04  
**Current stage:** Technical deployment candidate  
**Formal go-live ready:** No  
**Permitted data:** Synthetic only

## Implemented

- [x] Approved source-class/domain controls and prohibited source types.
- [x] Version/hash change detection and no-change suppression.
- [x] Snapshot, timestamp, authority, provenance and exact citation validation.
- [x] Verified/pending/conflict/partial/blocked evidence states.
- [x] Materiality/confidence routes and high-impact human approval.
- [x] Manual signal creation restriction.
- [x] PFM focus, API/UI, synthetic scenario, nine tests and hardened container.
- [x] Product, assurance, UAT, operations and deployment documentation.

| Gate | Status | Remaining accountable work |
|---|---|---|
| L0 — Strategy and ownership | Partial | Approve sponsor, owner, scope, benefits and funding |
| L1 — Product and process | Technical ready; approval pending | Approve detection workflow, categories, outputs, exclusions and service levels |
| L2 — Data and evidence | Synthetic baseline | Approve real source corpus, ownership, rights, official lineage, quality, retention and citation rules |
| L3 — AI and knowledge | Deterministic baseline | Build/validate fetch/OCR/diff/classification services; calibrate precision, recall, confidence and thresholds |
| L4 — Governance and compliance | Partial | Approve PFM/policy decision rights, high-impact review, exception sources and legal obligations |
| L5 — Security and privacy | Baseline | Implement enterprise IAM, egress/SSRF/content controls, encryption, immutable audit and security testing |
| L6 — Architecture and integration | Candidate | Provision orchestration, workers, stores, source/P03 adapters, schedules and observability |
| L7 — Verification and assurance | CI, nine P04 tests, compile, image build and live smoke test passed | Complete corpus, citation, security, performance, accessibility and resilience assurance |
| L8 — Operating model | Template ready | Name source/analyst/PFM/approval/support owners; approve SLA/SLO, RTO/RPO and procedures |
| L9 — Deployment and resilience | Container candidate | Validate target CI/CD, signing, backup/restore, capacity, continuity and rollback |
| L10 — Go-live authority and value | Not started | Complete UAT, residual-risk acceptance and final production authorization |

See [evidence](docs/GO-LIVE-EVIDENCE.md), [PFM alignment](docs/PFM-ALIGNMENT.md), [UAT](docs/UAT.md) and [portfolio standard](../../docs/GO-LIVE-GATE-STANDARD.md).
