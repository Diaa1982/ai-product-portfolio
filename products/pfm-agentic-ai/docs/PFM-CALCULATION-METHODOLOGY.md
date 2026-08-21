# PFM Calculation Methodology

All values are currency-neutral and must use the same approved basis, period and unit.

| Measure | Formula | Default alert |
|---|---|---|
| Available balance | revised budget − actuals − commitments | `< 0` |
| Utilization % | actuals ÷ revised budget × 100 | `> 95%` |
| Commitment pressure % | commitments ÷ revised budget × 100 | reported, locally governed |
| Absolute variance % | abs(actuals − period plan) ÷ abs(period plan) × 100 | `> 20%` |
| Liquidity gap | cash available − obligations due | `< 0` |
| Budget exceedance | actuals + commitments > revised budget | true |

When revised budget is zero, utilization and commitment pressure return null. When period plan is zero, variance returns null and routes to specialized review. Threshold equality does not trigger an “above” alert. Production owners must approve currency, consolidation, accrual/cash basis, period cut-off, commitment definition, tolerance, rounding and exception treatment.
