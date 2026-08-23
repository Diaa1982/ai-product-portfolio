# P12 — Revenue Reconciliation AI

Revenue Reconciliation AI is a deterministic, evidence-led reconciliation product for revenue receipts, refunds, fraud adjustments, commissions, VAT components, settlement, bank matching and exception routing.

**Status:** technical deployment candidate; dummy/sample data only; not approved for production, treasury transfer, tax determination or accounting posting.

## Implemented MVP

- Original POC forms: `Frm.601.2025.01`, `Frm.172.2024.02`, `Frm.221.2018.01`.
- Form 601: Settlement = Received − Refund − Fraud; Total invoice = Commission + VAT; Net transfer = Settlement − Total invoice.
- Fixed AED 100, fixed AED 100 plus 5% VAT, and agreed-percentage patterns.
- Form 172 agreed-percentage-only validation; Form 221 record coverage for all three configured types.
- e-Pay/internal-to-bank exact, unmatched-reference, discount-variance and amount-variance classification.
- Evidence, duplicate, period/currency, bank-account, SoD, materiality and expected-result controls.
- Protected-action denial for refunds, write-offs, tax eligibility, fee/commission changes, journals and transfers.
- API and Revenue Reconciliation Workbench at `/p12`.

## Run

```bash
docker compose -f products/revenue-reconciliation-ai/deploy/docker-compose.yml up --build
```

Open `http://localhost:8080/p12`.

## Documentation

- [PRD](docs/PRD.md), [architecture](docs/ARCHITECTURE.md), [process and controls](docs/PROCESS-AND-CONTROLS.md)
- [Calculation methodology](docs/CALCULATION-METHODOLOGY.md), [matching methodology](docs/MATCHING-METHODOLOGY.md), [form rules](docs/FORM-RULES.md)
- [Governance matrix](docs/CONTROL-RISK-GOVERNANCE-MATRIX.md), [data model](docs/DATA-MODEL.md), [API](docs/API.md)
- [Security](docs/SECURITY-PRIVACY.md), [deployment](docs/DEPLOYMENT.md), [runbook](docs/RUNBOOK.md)
- [Test plan](docs/TEST-PLAN.md), [UAT](docs/UAT.md), [roadmap](docs/ROADMAP.md), [go-live evidence](docs/GO-LIVE-EVIDENCE.md)

## Authority boundary

The responsible employee validates the result and exceptions. Authorized revenue, treasury, tax and accounting officials retain all decisions. Configuration values are preserved from the synthetic POC and must be validated against current approved agreements, policies and delegations before any production use.
