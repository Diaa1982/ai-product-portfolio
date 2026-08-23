# Agent Cards

The machine-readable source is [`../config/pfm-agents.v1.json`](../config/pfm-agents.v1.json). Each card must be approved and mapped to local responsibilities before production.

| Agent | Decision-support output | Human gate | Prohibited authority |
|---|---|---|---|
| Fiscal Strategy & Planning | Scenarios, assumptions, fiscal-risk brief | PFM process owner | Adopt fiscal policy or approve a budget |
| Budget Preparation | Validation, costing and allocation options | Budget authority | Approve appropriation or reallocation |
| Budget Execution & Commitments | Variance, pressure and balance exceptions | Budget authority | Release funds or approve commitment |
| Revenue Management | Collection variance, forecast and exceptions | PFM process owner | Assess tax, change fees, approve refunds/write-offs or penalties |
| Treasury & Cash | Forecast, liquidity alert and options | Treasury authority | Release funds or authorize payment |
| Debt & Fiscal Risk | Risk classification and scenarios | PFM process owner | Borrow, guarantee or execute a debt transaction |
| Accounting & Reporting | Reconciliation/reporting exceptions | Accounting authority | Approve journals, close periods, certify balances or publish statements |
| Internal Control & Audit Follow-up | Gaps and remediation status | Audit authority | Issue an audit opinion or close a finding |
| Performance & Executive Reporting | Validated executive brief | Executive authority | Make or implement the underlying financial decision |

Every card requires purpose, owner, trigger, inputs, source authority, outputs, success criteria, allowed next agents, human gate, prohibited actions, failure route, evidence standard, retention, monitoring and change owner.
