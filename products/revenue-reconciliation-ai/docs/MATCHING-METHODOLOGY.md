# Matching Methodology

- `MATCHED`: references equal and amount variance is within AED 0.01.
- `UNMATCHED_REFERENCE`: internal/e-Pay and bank references differ; high-severity review.
- `MATCHED_WITH_DISCOUNT_VARIANCE`: references equal and bank amount is below internal amount beyond tolerance; discount evidence required.
- `MATCHED_WITH_AMOUNT_VARIANCE`: references equal and bank amount is above internal amount beyond tolerance.
- Duplicate internal or bank flags block the record.

No fuzzy/probabilistic matching is implemented. A later model requires labeled ground truth, approved confidence/accuracy thresholds, explainability, false-match controls and human confirmation. Matching never proves entitlement, fraud, tax eligibility or authorization.
