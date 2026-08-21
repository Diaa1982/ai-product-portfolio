# AI Governance Control Tower

**Product ID:** P14  
**Release:** 1.0.0 technical deployment candidate  
**Formal go-live:** Not approved  
**Data:** Synthetic only

P14 governs the AI portfolio through proportional risk tiers, G0–G4 gates, control evidence, accountable human approvals, monitoring incidents, safe shutdown and benefits oversight. It aligns to ISO/IEC 42001 concepts without claiming certification.

## Working capabilities

- Low, Moderate, High and Critical risk classification.
- Explicit block on autonomous payments, transfers, journal postings, budget adjustments, financial certification, financial-statement publication and risk acceptance.
- G0 Intake → G1 Value/Risk → G2 Design/Data/Controls → G3 Independent Validation → G4 CEO Production Authorization.
- Cumulative risk-tier control requirements and evidence completeness.
- Mandatory QA before G3/G4 and independent testing for High/Critical systems.
- Human-only gate decisions; CEO is final G4 approver.
- Monitoring for security, privacy, unauthorized action, financial-control, audit, fairness, explainability, performance and drift events.
- Safe shutdown/incident command for critical breaches.
- Dedicated `/p14` dashboard, API, tests, synthetic decision pack and hardened container.

## Run

```bash
docker compose -f products/ai-governance-control-tower/deploy/docker-compose.yml up --build
```

Open `/p14`; OpenAPI is at `/docs`.

## Documents

[PRD](docs/PRD.md) · [Architecture](docs/ARCHITECTURE.md) · [Risk method](docs/RISK-METHODOLOGY.md) · [Gate standard](docs/GATE-STANDARD.md) · [Control catalog](docs/CONTROL-CATALOG.md) · [Registers](docs/REGISTERS.md) · [ISO 42001 alignment](docs/ISO-42001-ALIGNMENT.md) · [PFM alignment](docs/PFM-ALIGNMENT.md) · [Board procedure](docs/BOARD-OPERATING-PROCEDURE.md) · [Security](docs/SECURITY-PRIVACY.md) · [Deployment](docs/DEPLOYMENT.md) · [Runbook](docs/RUNBOOK.md) · [Tests](docs/TEST-PLAN.md) · [UAT](docs/UAT.md) · [Evidence](docs/GO-LIVE-EVIDENCE.md) · [Checklist](GO-LIVE-CHECKLIST.md)
