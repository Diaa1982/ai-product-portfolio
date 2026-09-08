# P01 — PFM Agentic AI

PFM Agentic AI is a governed fiscal-intelligence and workflow platform for the public finance management cycle. The current release provides a **functional management demonstration** that combines successfully retrieved authoritative public signals with a coherent synthetic government fiscal environment. AI prepares analysis, scenarios, explanations and controlled handoffs; accountable officials retain protected legal, budget, treasury, accounting and reporting authority.

**Status:** management-demo candidate; live public external signals + synthetic internal fiscal data; not approved for production financial processing.

## Management-demo capabilities

- Animated global/regional/local **Fiscal Signal Radar** with source provenance and explicit degraded-source behavior.
- Live external evidence kept separate from AI interpretation and simulated fiscal impact.
- Governed **Agent Operations workflow** and runtime activity trail.
- Synthetic entity fiscal model covering approved/adjusted budget, actuals, commitments, forecast, accrual, cash, delays and funding needs.
- Scenario engine: baseline, revenue shock, capital delay, cash pressure and accounting-close exception.
- Treasury liquidity horizon and protected approval gate.
- Budget ↔ cash ↔ accrual fiscal-position bridge.
- **Ask PFM** executive query interface over governed synthetic evidence.
- Variable report factory by report type, entity, mandate and period.
- Demo reset for repeatable management presentations.
- Existing nine-agent PFM orchestration/configuration and protected-action controls retained in the repository.

## Run

```bash
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml up --build
```

Open:

- `http://localhost:8080/` — management demo.
- `http://localhost:8080/command-center` — agent command center.
- `http://localhost:8080/docs` — API.

## Documentation

- [Management demo](docs/MANAGEMENT-DEMO.md)
- [Product requirements](docs/PRD.md)
- [Operating blueprint](docs/OPERATING-BLUEPRINT.md)
- [Agent cards](docs/AGENT-CARDS.md)
- [Workflow](docs/WORKFLOW.md)
- [Control, risk and governance matrix](docs/CONTROL-RISK-GOVERNANCE-MATRIX.md)
- [Calculation methodology](docs/PFM-CALCULATION-METHODOLOGY.md)
- [PEFA and IPSAS alignment](docs/PFM-PEFA-IPSAS-ALIGNMENT.md)
- [API](docs/API.md), [data model](docs/DATA-MODEL.md), [security](docs/SECURITY-PRIVACY.md)
- [Deployment](docs/DEPLOYMENT.md), [runbook](docs/RUNBOOK.md), [test plan](docs/TEST-PLAN.md), [UAT](docs/UAT.md)
- [Roadmap](docs/ROADMAP.md), [go-live evidence](docs/GO-LIVE-EVIDENCE.md), [checklist](GO-LIVE-CHECKLIST.md)

## Authority boundary

Configuration roles are generic design placeholders. Before production, the organization must map every role and gate to applicable law, policy, delegation and segregation-of-duties rules. AI output is analysis or recommendation—not an appropriation, fund release, payment authorization, accounting certification, legal determination, financial-statement approval/publication or audit opinion.
