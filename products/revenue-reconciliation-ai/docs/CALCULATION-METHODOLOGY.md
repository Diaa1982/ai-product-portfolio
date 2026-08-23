# Calculation Methodology

| Measure | Rule |
|---|---|
| Settlement | Received Amount − Refund Amount − Fraud Transactions |
| Fixed commission | AED 100 |
| Agreed-percentage commission | Settlement × configured commission rate % |
| Zero VAT | AED 0 |
| Fixed-100 VAT | AED 100 × 5% = AED 5 |
| Agreed-percentage VAT | Commission × configured VAT rate % |
| Total invoice | Commission + VAT |
| Net transfer | Settlement − Total invoice |
| Bank variance | Bank amount − Internal amount |
| Discount amount | max(0, Internal amount − Bank amount) |

The fixed values reproduce the dummy POC requirements. They are not tax, fee, accounting or contractual determinations. Production owners must approve agreement applicability, rates, tax treatment, rounding, effective dates, sign convention, materiality and tolerance.
