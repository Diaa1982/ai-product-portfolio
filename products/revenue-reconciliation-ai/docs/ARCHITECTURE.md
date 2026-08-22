# Architecture

1. **Controlled intake:** synthetic structured records representing e-Pay Dashboard, Settlement, bank-statement and commission-bank data; manual Excel/PDF intake may be added in pilot.
2. **Canonical transaction layer:** provider, bank accounts, period/currency, references, receipt/refund/fraud, commission/VAT and evidence.
3. **Deterministic calculation:** settlement, commission, VAT, invoice, net transfer and expected-result reconciliation.
4. **Matching:** exact reference/amount, unmatched reference, discount variance, amount variance and duplicates.
5. **Exception workflow:** responsible employee, reviewer, evidence, materiality, approval and escalation.
6. **Assurance:** versioned configuration, calculation digest, audit, monitoring, rollback and manual fallback.

Production source, bank, treasury, revenue, accounting, SharePoint/email adapters and persistent stores require separate owner-approved design. The analytical layer never executes the transfer or financial adjustment.
