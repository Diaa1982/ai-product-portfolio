# P12 — Revenue Reconciliation AI Go-Live Checklist

Status: **technical deployment candidate — dummy/sample-only; not production-approved**.

Technical verification: [Portfolio Quality run 70](https://github.com/Diaa1982/ai-product-portfolio/actions/runs/32545755704) passed all 112 repository tests and all nine container/API smoke paths on 2026-08-22.

| Gate | Technical candidate evidence | Requirement before go-live |
|---|---|---|
| L0 Strategy/ownership | Purpose, scope and roadmap | Approve sponsor, owners, case, benefits and deployment scope |
| L1 Product/process | PRD, process and form controls | Approve E2E process, RACI, SLA, manual fallback and excluded decisions |
| L2 Data/evidence | Structured model, sources and synthetic case | Approve source/bank fields, owners, quality, lineage, evidence and retention |
| L3 Rules/models | Deterministic calculations/matching | Approve current forms, agreements, rates, tolerances and model evaluations if added |
| L4 Governance/compliance | SoD, human gates and protected actions | Approve revenue/treasury/tax/accounting decision rights and requirements |
| L5 Security/privacy | Security baseline | Implement SSO/RBAC, encryption/masking, secure intake and testing |
| L6 Architecture/integration | API, workbench and container | Build approved source/bank/treasury/accounting adapters and persistent stores |
| L7 Verification | 15 focused tests | Ground truth, false-match/accuracy, contract, scale, security, resilience and UAT |
| L8 Operating model | Runbook and monitoring | Approve support, exception ownership/SLA, training and rule/change governance |
| L9 Deployment/resilience | Hardened container | Approved environments, CI/CD, signing/scanning, backup/DR and rollback |
| L10 Go-live/value | Evidence register and pilot roadmap | Pilot, residual-risk acceptance, formal authorization and benefits review |

No gate or output authorizes a refund, write-off, tax treatment, ledger change, payment or treasury transfer.
