# MVP Operating Guide

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.portfolio_api.main:app --reload
```

Open `http://127.0.0.1:8000` for the portfolio dashboard or `/docs` for the API interface.

## Controlled workflow

1. Create a case using a configured product and required inputs.
2. Attach approved, classified evidence with a content hash and source version.
3. Run the product evaluation.
4. Review findings, calculations, risks and recommendations.
5. Submit the case to the configured approval gate.
6. The required accountable role approves, rejects or returns the case.
7. Verify the hash-chained audit log.

## PFM calculation profile

The executable baseline calculates:

- Variance = actual − budget.
- Utilization = actual ÷ budget.
- Available balance = budget − actual − commitments.
- Commitment pressure = commitments ÷ budget.

Negative available balance pauses the case as critical. Material findings require evidence before approval submission.

## AI use-case scoring

The baseline uses the approved weighting approach:

- Value: 60%.
- Feasibility: 40%.

The threshold is configurable in `products/workflows.json`; the baseline minimum is 3.0.

## Operating constraints

- Recommend and draft only.
- Human approval remains mandatory for financial authority and consequential actions.
- Only synthetic data is permitted in the baseline.
- Every material finding requires evidence.
- Agent handoffs, evaluations and decisions must remain traceable.
- Critical cases pause and cannot bypass the approval workflow.

## Environment variables

| Variable | Purpose |
|---|---|
| `PRODUCT_REGISTRY_PATH` | Machine-readable portfolio register |
| `WORKFLOW_PATH` | Product workflow definitions |
| `CASE_STORE_PATH` | Local JSON case store for MVP use |
| `DASHBOARD_PATH` | Portfolio dashboard HTML |

The JSON store is for controlled MVP use only. A production implementation must use an approved database, identity provider, immutable audit service and enterprise secret store.
