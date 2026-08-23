# Portfolio Go-Live Gate Standard

A project is **go-live ready** only when every mandatory gate has documented evidence and accountable approval. Passing technical tests alone is insufficient.

| Gate | Area | Minimum go-live evidence |
|---|---|---|
| L0 | Strategy and ownership | Approved outcome, sponsor, product owner, users, scope, funding and benefits |
| L1 | Product and process | Approved PRD, AS-IS/TO-BE process, AI-versus-human tasks, acceptance criteria and excluded decisions |
| L2 | Data and evidence | Data owner, classification, lawful use, source/field mapping, quality thresholds, retention and lineage |
| L3 | AI and knowledge | Approved models/rules/prompts, grounding sources, evaluation set, thresholds, versioning and rollback |
| L4 | Governance and compliance | Decision rights, human oversight, risk tier, legal/policy review and standards mapping |
| L5 | Security and privacy | Threat model, IAM, least privilege, encryption, secrets, vulnerability testing, PII controls and incident response |
| L6 | Architecture and integration | Approved target architecture, APIs/events, environments, source/target integrations and observability |
| L7 | Verification and assurance | Functional, calculation, model, security, performance, accessibility, DR and UAT evidence |
| L8 | Operating model | RACI, support ownership, SLAs, monitoring, change/release management, training and user procedures |
| L9 | Deployment and resilience | Production infrastructure, CI/CD, backup, recovery, capacity, continuity and rollback |
| L10 | Go-live authority and value | Formal go-live decision, residual-risk acceptance, KPI baseline, benefits plan and post-implementation review |

## Standards baseline

Apply relevant requirements from PEFA-oriented PFM practices, IPSAS, ISO 9001, ISO/IEC 42001, ISO/IEC 23894, ISO/IEC 27001, ISO/IEC/IEEE 42010 and the NIST AI RMF. Applicability must be confirmed for each deployment.

## Readiness status

- **Ready:** gate evidence approved.
- **Partial:** baseline components exist but approval/evidence is incomplete.
- **Not started:** no deployment-specific evidence.
- **Blocked:** external authority, data, integration, legal or security dependency prevents completion.
- **Not applicable:** documented justification approved.

All 18 projects currently remain **not go-live ready**. They have an executable synthetic-data platform foundation, not a production authorization.
