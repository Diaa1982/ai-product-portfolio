# Integrated IT Management AI

**Product ID:** P16  
**Category:** Enterprise Architecture & Technology Management  
**Maturity:** Technical deployment candidate  
**Data policy:** Synthetic only  
**Production ready:** No

P16 creates an evidence-led management view across IT strategy, demand, portfolio/project delivery, architecture, services, incidents, changes, assets/configuration, continuity, security, risk, compliance, audit, suppliers, finance, workforce, knowledge and benefits.

## Executable scope

- Canonical, vendor-neutral records for services, work items, configuration items, portfolio items, risks, controls, evidence and decisions.
- Deterministic SLA, incident, change, configuration, portfolio and control indicators.
- Data-quality, evidence, ownership and cross-domain linkage exceptions.
- Weighted integrated-health view with visible inputs and weights.
- Draft recommendations and a human decision package.
- Protected-action enforcement for consequential IT decisions.
- FastAPI endpoints, dashboard, synthetic fixture, tests and hardened container baseline.

## Human-accountability boundary

The product may extract, compare, classify, calculate, summarize and recommend. It cannot deploy to production, approve a change, close an incident, accept risk, approve an SLA/budget/go-live, sign a contract, select a vendor, retire a service/asset or disable a control. Those actions require authorized workflows and recorded human approval.

## Run locally

`python -m unittest tests.test_p16_it_management -v`  
`uvicorn src.portfolio_api.main:app --reload`  
Open `http://127.0.0.1:8000/p16`.

Framework names are alignment references, not certification claims. See [PRD](docs/PRD.md), [architecture](docs/ARCHITECTURE.md), [data model](docs/CANONICAL-DATA-MODEL.md), [API](docs/API.md), [runbook](docs/RUNBOOK.md) and [go-live checklist](GO-LIVE-CHECKLIST.md).
