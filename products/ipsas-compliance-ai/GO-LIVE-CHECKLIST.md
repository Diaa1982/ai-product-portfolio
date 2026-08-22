# P11 — IPSAS Compliance AI Go-Live Checklist

Status: **technical deployment candidate — synthetic-only; no formal IPSAS conclusion; not production-approved**.

Technical verification: [Portfolio Quality run 68](https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32543590926) passed all 97 repository tests and all eight container/API smoke paths on 2026-08-22.

| Gate | Technical candidate evidence | Requirement before go-live |
|---|---|---|
| L0 Strategy/ownership | Purpose, scope and roadmap | Approve sponsor, product/accounting owners, business case, benefits and scope |
| L1 Product/process | PRD, methodology and human boundaries | Approve journal/reconciliation/disclosure workflows, SLA and manual fallback |
| L2 Data/evidence | Structured model, synthetic cases and evidence controls | Approve sources, files, owners, quality, lineage, classification and retention |
| L3 Knowledge/models | Controlled-knowledge standard and deterministic checks | Approve applicable content, licensing, versions, retrieval/extraction and evaluations |
| L4 Governance/compliance | Protected actions, SoD and review gates | Approve materiality, policies, decision rights and applicable requirements |
| L5 Security/privacy | Security baseline documented | Implement SSO/RBAC, secure file intake, encryption, privacy and testing |
| L6 Architecture/integration | API, workbench and container | Build approved ledger/reconciliation/reporting/knowledge/approval integrations |
| L7 Verification | 15 focused tests and evaluation targets | Expert ground truth, ≥90% approved agreement, security/performance/resilience/UAT |
| L8 Operating model | Runbook and monitoring | Approve RACI, support, training, knowledge/model/data/change governance |
| L9 Deployment/resilience | Hardened container baseline | Approved environments, CI/CD, signing/scanning, backup/DR and rollback |
| L10 Go-live/value | Evidence register and pilot roadmap | Pilot, residual-risk acceptance, formal authorization and benefits review |

No gate or system output approves an accounting treatment, journal, period close, balance, financial statement or publication.
