# User Acceptance Testing

Use dummy/sample or formally approved masked data.

| Scenario | Expected result |
|---|---|
| Form 601 fixed 100 + 5% | Settlement, AED 100 commission, AED 5 VAT, invoice and net reconcile |
| Form 172 non-agreed type | Blocked |
| Form 221 configured types | Accepted for record; no tax-eligibility decision |
| Internal vs bank exact match | `MATCHED` |
| Same reference/lower bank amount | Discount variance with evidence/reviewer route |
| Different reference | High unmatched exception and approval interruption |
| Duplicate/missing evidence/invalid context | Blocked |
| Material/negative result | Human review; no transfer/refund/posting |
| Protected action | Autonomous execution denied |

Sign-off requires revenue operations, responsible employee/process owner, treasury, accounting, tax/legal where applicable, data, technology, security/privacy and internal control. UAT does not authorize financial execution.
