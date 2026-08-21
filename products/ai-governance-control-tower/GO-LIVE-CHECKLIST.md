# AI Governance Control Tower — Go-Live Readiness Checklist

**Product ID:** P14  
**Current stage:** Technical deployment candidate  
**Formal go-live ready:** No  
**Permitted data:** Synthetic only

## Implemented

- [x] Low/Moderate/High/Critical risk tiers and cumulative controls.
- [x] G0–G4 evidence gates and human-only approvals.
- [x] Mandatory QA and independent High/Critical testing.
- [x] CEO-only G4 production authorization.
- [x] PFM autonomous financial-action blocks.
- [x] Monitoring incidents, pause and safe shutdown.
- [x] ISO 42001/PFM alignment, board procedure and register definitions.
- [x] API/UI, synthetic cases, eleven tests and hardened container.
- [x] Security, deployment, operations, UAT and evidence documentation.

| Gate | Status | Remaining accountable work |
|---|---|---|
| L0 — Strategy and ownership | Partial | Approve sponsor, product owner, charter, scope, funding and value baseline |
| L1 — Product and process | Technical ready; approval pending | Approve PRD, risk/gate model, decision rights, exclusions and service levels |
| L2 — Data and evidence | Synthetic baseline | Approve register schemas, owners, classifications, evidence retention/lineage and production data |
| L3 — AI and knowledge | Deterministic baseline | Approve policy/control configuration; integrate inventories/models/agents; validate change/reassessment rules |
| L4 — Governance and compliance | Candidate documented | Approve board/council/design/risk/assurance/CEO authorities, legal obligations, exceptions and ISO alignment |
| L5 — Security and privacy | Baseline | Implement enterprise IAM/step-up approval, encryption, immutable audit/evidence and complete security/privacy testing |
| L6 — Architecture and integration | Candidate | Provision databases/registers, workflow/event integrations, P08/product connectors and observability |
| L7 — Verification and assurance | CI, eleven P14 tests, compile, image build and live risk/incident smoke tests passed | Complete policy, RBAC, integration, security, performance, accessibility and resilience assurance |
| L8 — Operating model | Template ready | Name governance/operations owners; approve committee procedure, SLA/SLO, RTO/RPO, training and escalation |
| L9 — Deployment and resilience | Container candidate | Validate target CI/CD, image signing, backup/restore, continuity and rollback exercises |
| L10 — Go-live authority and value | Not started | Complete UAT, residual-risk acceptance, governance approvals and CEO production authorization |

See [go-live evidence](docs/GO-LIVE-EVIDENCE.md), [gate standard](docs/GATE-STANDARD.md), [PFM alignment](docs/PFM-ALIGNMENT.md), [UAT](docs/UAT.md) and [portfolio standard](../../docs/GO-LIVE-GATE-STANDARD.md).
