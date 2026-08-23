# Corporate Performance Review AI

**Product ID:** P09  
**Release:** 1.0.0 technical deployment candidate  
**Formal go-live:** Not approved  
**Data:** Synthetic only

P09 validates KPI master/results data, calculates governed performance status, separates review narratives, manages corrective-action evidence and produces draft management/executive reviews across enterprise, sector and division levels.

## Working capabilities

- Required KPI master/result schema and permanent KPI ID.
- Direction-aware Higher, Lower and Exact calculations.
- Controlled routing for Range, Milestone, Binary, zero-target and negative-value KPIs.
- Configurable default bands: Exceeded ≥105%, Achieved 100–<105%, Attention 90–<100%, Off Target <90%.
- Official results require evidence reference and approval date.
- Source-row hash, data cut-off, trend and review-calendar timeliness.
- Separate facts, calculations, owner explanations, inferences and recommendations.
- Corrective-action completeness and human approvals.
- Target treatments Retain/Stretch/Recalibrate/Redesign/Rebaseline; all proposed targets marked NOT APPROVED.
- Dedicated `/p09` dashboard/API, tests, synthetic scenario and hardened container.

## Run

```bash
docker compose -f products/corporate-performance-review-ai/deploy/docker-compose.yml up --build
```

## Documents

[PRD](docs/PRD.md) · [KPI data standard](docs/KPI-DATA-STANDARD.md) · [Calculation method](docs/CALCULATION-METHODOLOGY.md) · [Review method](docs/REVIEW-METHODOLOGY.md) · [PFM alignment](docs/PFM-ALIGNMENT.md) · [Data model](docs/DATA-MODEL.md) · [API](docs/API.md) · [Security](docs/SECURITY-PRIVACY.md) · [Deployment](docs/DEPLOYMENT.md) · [Runbook](docs/RUNBOOK.md) · [Tests](docs/TEST-PLAN.md) · [UAT](docs/UAT.md) · [Evidence](docs/GO-LIVE-EVIDENCE.md) · [Checklist](GO-LIVE-CHECKLIST.md)
