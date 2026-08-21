# AI Product Portfolio

Private monorepo for converting a portfolio of public finance management, enterprise operations, process, service, governance, assurance, and strategic decision-support initiatives into governed AI products.

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
