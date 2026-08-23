# Strategic Radar

**Product ID:** P03  
**Release:** 1.0.0 technical deployment candidate  
**Formal go-live status:** Not approved  
**Current data:** Synthetic only

Strategic Radar is a governed intelligence product for horizon scanning, signal detection and evidence-led recommendations. It serves government and business audiences, with an explicit Public Finance Management lens across fiscal policy, budget, treasury, revenue, central accounts, debt, expenditure, commitments, financial control, performance and fiscal sustainability.

## Working capabilities

- Official-source registry with approval, status and domain allowlisting.
- Deterministic evidence/provenance verification that blocks unsupported material claims.
- Version-change record and immutable SHA-256 evidence reference.
- Six-factor 0–1 materiality scoring: scope, breadth, time sensitivity, evidence strength, novelty and stakeholder relevance.
- Routes: auto-alert eligible ≥0.82; analyst review 0.55–0.81 or any null criterion; low priority <0.55.
- Separate fact, interpretation and advisory recommendation layers.
- Human approval for high-impact alerts, policy advice, executive delivery, trusted memory and low-confidence executive sharing.
- Dedicated `/p03` interface, API, tests, synthetic scenario and container package.

## Run

```bash
docker compose -f products/strategic-radar/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p03`; OpenAPI is at `/docs`.

## Documents

[PRD](docs/PRD.md) · [Architecture](docs/ARCHITECTURE.md) · [PFM alignment](docs/PFM-ALIGNMENT.md) · [Source governance](docs/SOURCE-GOVERNANCE.md) · [Data model](docs/DATA-MODEL.md) · [Materiality](docs/MATERIALITY-METHODOLOGY.md) · [API](docs/API.md) · [Security](docs/SECURITY-PRIVACY.md) · [Deployment](docs/DEPLOYMENT.md) · [Runbook](docs/RUNBOOK.md) · [Test plan](docs/TEST-PLAN.md) · [UAT](docs/UAT.md) · [Evidence](docs/GO-LIVE-EVIDENCE.md) · [Checklist](GO-LIVE-CHECKLIST.md)

The product provides advisory intelligence only. It cannot issue policy, change fiscal assumptions, commit public resources or execute an action autonomously.
