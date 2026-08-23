# User Acceptance Testing

Use synthetic or formally approved masked data in a segregated test environment.

| Scenario | Expected result |
|---|---|
| Valid execution-to-treasury case | Correct metrics; `READY`; complete evidence/audit event |
| Validation fails or evidence missing | `BLOCKED`; remediation route; downstream agent does not start |
| Invalid agent transition | `BLOCKED` with transition issue |
| Variance >20% or utilization >95% | Correct alert and at least Medium risk |
| Negative balance, budget exceedance or liquidity gap | High risk and approval interruption |
| Valid high-risk human approval reference | Interruption cleared; handoff may be `READY` if all other controls pass |
| Protected financial/accounting/audit action | Autonomous execution denied |
| Zero period plan | Null variance and specialized-review alert |

Sign-off requires product owner, relevant PFM process owners, data owner, security/privacy, internal control, technology operations and applicable accounting/audit reviewers. Sign-off confirms only the approved scope and does not delegate statutory authority.
