# P01 — PFM Agentic AI

PFM Agentic AI is a controlled decision-support and workflow layer for the public finance management cycle. Nine functional agents prepare validated analysis, alerts and evidence-led handoffs. The orchestrator blocks invalid transitions and high-risk handoffs without a human approval reference.

**Status:** technical deployment candidate; synthetic data only; not approved for production.

## MVP capabilities

- Data validation and evidence requirements before downstream work begins.
- Budget variance, utilization, commitment pressure, available balance and cash-liquidity calculations.
- Fiscal-risk classification, approval interruption and escalation routing.
- Accounting/reporting exception and audit follow-up workflow design.
- Complete handoff audit event: payload, success criteria, workflow state, result, interruption and failure route.
- Explicit denial of autonomous protected financial and professional actions.
- Interactive command center at `/p01` and OpenAPI endpoints.

## Run

```bash
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p01`. All included examples are synthetic.

## Documentation

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

Configuration roles are generic design placeholders. Before production, the organization must map every role and gate to applicable law, policy, delegation and segregation-of-duties rules. AI output is analysis or recommendation—not an approval, authorization, certification, legal determination, financial statement publication, or audit opinion.
