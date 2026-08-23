# Product Requirements

## Outcome

Reduce manual reconciliation effort and improve traceability between e-Pay/internal revenue records, settlement reports, bank statements and commission data while preserving financial-control accountability.

## MVP requirements

1. Support the three original POC forms and their controlled scope.
2. Calculate settlement, commission, VAT, invoice and net transfer deterministically.
3. Compare internal/e-Pay and bank references/amounts and classify matches/exceptions.
4. Detect duplicate, missing-evidence, invalid context, SoD, materiality and expected-result failures.
5. Separate facts, calculations, exceptions, assumptions, recommendations and evidence.
6. Require human review for high/material exceptions and deny autonomous protected actions.
7. Provide versioned API, workbench, synthetic scenario, tests and container.

## Non-goals

No refund initiation/approval, receivable write-off, fraud confirmation, tax eligibility/determination, fee/commission agreement change, ledger posting/adjustment, exception closure, payment authorization or treasury transfer. Live source integrations and probabilistic matching are outside the deterministic MVP.
