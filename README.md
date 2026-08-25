# AI Product Portfolio

Private monorepo for converting a portfolio of public finance management, enterprise operations, process, service, governance, assurance, and strategic decision-support initiatives into governed AI products.

## Portfolio productization status

All 18 products now have technical deployment-candidate baselines. This means documented, tested, synthetic-only software candidates—not production authorization. Every product remains `production_ready: false` pending organizational data, integration, IAM/security/privacy, UAT, operations, residual-risk and formal go-live gates.

## Portfolio control center and Develop-stage closure

- [Open the live AI Product Portfolio Control Center](https://ai-product-portfolio-hub.diaa-alkhateeb.chatgpt.site).
- Complete deployable source is version-controlled in [\`portfolio-control-center/\`](portfolio-control-center/).
- [Develop-stage closure](docs/DEVELOP-STAGE-CLOSURE.md) records the completed baseline and remaining Deploy-gate controls.
- [Owner input register](docs/OWNER-INPUT-REGISTER.md) identifies the decisions and evidence required before pilot and go-live.
- [Knowledge-management guide](docs/KNOWLEDGE-MANAGEMENT.md) links GitHub, Notion, and the operational control center.

## Executable portfolio MVP

The platform now provides:

- 18 configured product workflows.
- Shared case, evidence, finding, recommendation and approval records.
- PFM execution calculations for variance, utilization, available balance and commitment pressure.
- Configurable AI use-case scoring using 60% value and 40% feasibility.
- Evidence requirements for material findings.
- Automatic pause for critical cases.
- Role-enforced approval decisions.
- Hash-chained, verifiable audit events.
- FastAPI endpoints and an integrated portfolio dashboard.
- Synthetic end-to-end demonstration cases.
- Automated product, engine, API and confidentiality-control tests.

## Portfolio scope

- Public finance planning, budgeting, treasury, revenue, accounting, IPSAS reporting, audit, risk, and executive intelligence.
- Strategic radar, evidence-grounded signal detection, and controlled recommendation workflows.
- Enterprise process, service, performance, partnership, architecture, and IT-management intelligence.
- Shared AI governance, human approval, traceability, security, evaluation, and structured-output controls.

## Productization principles

1. Public value and accountable decision-making first.
2. Process and control design before automation.
3. Evidence-grounded AI with source provenance.
4. Human approval for consequential decisions.
5. IPSAS and PEFA-aligned PFM practices, ISO management-system principles, and auditable records.
6. Privacy, security, segregation of duties, and least privilege by design.
7. Synthetic data only until an approved data-onboarding process is completed.
8. Recommendations are separated from formal approvals and authorized transactions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.portfolio_api.main:app --reload
```

Open `http://127.0.0.1:8000` for the dashboard and `http://127.0.0.1:8000/docs` for the API.

For a controlled GitHub-run demonstration or readiness check, use the [Pilot Validation workflow](docs/PILOT-WORKFLOW.md). It builds one selected product, applies the synthetic-only boundary, performs smoke checks and publishes an evidence artifact; it does not deploy to production.

## Portfolio groups

Each project remains an independent package with its own product document and go-live checklist.

1. [PFM Intelligence & Financial Operations](groups/01-pfm-intelligence-financial-operations/README.md)
2. [PFM Architecture, Benchmarking & Maturity](groups/02-pfm-architecture-benchmarking-maturity/README.md)
3. [Strategy, Performance & AI Governance](groups/03-strategy-performance-ai-governance/README.md)
4. [Process, Service & Partnership Operations](groups/04-process-service-partnership-operations/README.md)
5. [Enterprise Architecture & Technology Management](groups/05-enterprise-architecture-technology/README.md)

Open the [categorized project catalog and go-live readiness matrix](docs/PROJECT-CATALOG.md) for direct links to every project document and its tailored checklist. The [standard go-live gates](docs/GO-LIVE-GATE-STANDARD.md) define the evidence required before any production launch.

## Repository map

- `products/` — product packages, registry and workflow configuration.
- `shared/` — reusable schemas, governance controls, prompts and evaluation standards.
- `docs/` — architecture, API, stage gates, roadmap and operating guidance.
- `src/` — shared executable API, workflow engine and dashboard.
- `synthetic/` — non-production demonstration cases.
- `tests/` — automated validation and control tests.
- `.github/workflows/` — quality and confidentiality checks.

## Information protection

The repository does not contain confidential government information, production financial data, internal evidence, credentials, or organization-specific datasets. Runtime case data is excluded from Git.

See [Product Register](docs/PRODUCT-REGISTER.md), [MVP Operating Guide](docs/MVP-OPERATING-GUIDE.md), [API Summary](docs/API.md), [Productization Roadmap](docs/PRODUCTIZATION-ROADMAP.md), and [Information Handling](docs/INFORMATION-HANDLING.md).
