# P02 — PFM Brain

PFM Brain is a governed fiscal intelligence and reconciliation layer across planning, budget, execution, revenue, cash, performance, risk, control and authority information. It produces traceable analytical records while preserving official systems and accountable human decision rights.

**Status:** technical deployment candidate; FY2026 synthetic data only; not approved for production or statutory reporting.

## Implemented MVP

- Controlled dataset profile: AED, eight divisions, 60 accounts, 1,500 transaction design baseline and 20 acceptance cases.
- Enforced load sequence: Organization Master and Chart of Accounts before Approved Budget and downstream domains.
- Deterministic revised-budget, available-budget, variance, revenue-shortfall, closing-cash, cash-buffer, KPI, control and residual-risk calculations.
- Duplicate, evidence, period, currency, identifier, reconciliation, authority and segregation-of-duties controls.
- Critical-value and protected-action human approval gates, including the synthetic AED 420 million rephase test.
- Separate facts, calculations, risks, assumptions, recommendations, evidence and audit digest.
- API and interactive Fiscal Intelligence Workbench at `/p02`.

## Run

```bash
docker compose -f products/pfm-brain/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p02`.

## Key documents

- [Product requirements](docs/PRD.md) and [architecture](docs/ARCHITECTURE.md)
- [Canonical data standard](docs/CANONICAL-PFM-DATA-STANDARD.md) and [data model](docs/DATA-MODEL.md)
- [Calculation methodology](docs/CALCULATION-METHODOLOGY.md) and [insight standard](docs/INSIGHT-AND-RECONCILIATION-STANDARD.md)
- [Control and governance](docs/CONTROL-AND-GOVERNANCE-MATRIX.md) and [PFM/PEFA/IPSAS alignment](docs/PFM-PEFA-IPSAS-ALIGNMENT.md)
- [API](docs/API.md), [security](docs/SECURITY-PRIVACY.md), [deployment](docs/DEPLOYMENT.md), [runbook](docs/RUNBOOK.md)
- [Test plan](docs/TEST-PLAN.md), [UAT](docs/UAT.md), [roadmap](docs/ROADMAP.md), [go-live evidence](docs/GO-LIVE-EVIDENCE.md)

## Accountability boundary

The product does not replace an FMIS/GRP, treasury, revenue, performance, risk, accounting or audit system. It cannot approve budgets, reallocations, rephasing, fund releases, payments, refunds, write-offs, journals, period close, certified balances, statements or audit decisions. Generic roles, thresholds and integrations must be mapped to approved organization-specific requirements before production.
