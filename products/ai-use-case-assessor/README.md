# AI Use Case Assessor

**Product ID:** P08  
**Category:** Strategy, Performance & AI Governance  
**Release:** 1.0.0 technical deployment candidate  
**Formal go-live status:** Not approved

P08 turns an AI idea into an evidence-led assessment across business value, feasibility, risk and governance. It supports client-led, diagnostic-led and hybrid discovery. It does not approve funding, risk acceptance, consequential automation or production deployment.

## Working product

- Dedicated interface at `/p08` and OpenAPI documentation at `/docs`.
- Versioned 60% value / 40% feasibility priority model.
- Four portfolio classes: Quick Win, Strategic Bet, Fill-In and Question Mark.
- Low/medium/high risk screening and insufficient-information routing.
- Lifecycle: Discover → Evaluate → Prioritize → Approve → Develop → Deploy → Operate → Retire.
- CEO-only approval enforcement for proposals, final client outputs, strategic/high-risk recommendations, service/rule or pricing changes and unresolved escalations.
- Synthetic scenario, automated unit tests and container deployment package.

## Run locally

```bash
docker compose -f products/ai-use-case-assessor/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p08`; health is available at `http://localhost:8080/health`.

## Product documents

| Document | Purpose |
|---|---|
| [PRD](docs/PRD.md) | Scope, users, outcomes and acceptance criteria |
| [Architecture](docs/ARCHITECTURE.md) | Components, boundaries and production target |
| [Data model](docs/DATA-MODEL.md) | Assessment, evidence and approval structures |
| [Scoring methodology](docs/SCORING-METHODOLOGY.md) | Criteria, weights, classes and governance |
| [API](docs/API.md) | Endpoints and example requests |
| [Security and privacy](docs/SECURITY-PRIVACY.md) | Threats, controls and production obligations |
| [Deployment](docs/DEPLOYMENT.md) | Build, configuration, health and rollback |
| [Runbook](docs/RUNBOOK.md) | Operations, incidents and recovery |
| [Test plan](docs/TEST-PLAN.md) | Automated and non-functional assurance |
| [UAT](docs/UAT.md) | Business acceptance scenarios and sign-off |
| [Go-live evidence](docs/GO-LIVE-EVIDENCE.md) | Evidence index and decision record |
| [Go-live checklist](GO-LIVE-CHECKLIST.md) | L0–L10 readiness position |

## Accountability boundary

The engine produces advisory scores and routing recommendations. Evidence owners validate inputs, control owners assess risk, and the human CEO remains the final approver for protected actions. Production access, identity, persistence, data sources, retention, monitoring and organization-specific approvals must be configured in the target environment before formal go-live.
