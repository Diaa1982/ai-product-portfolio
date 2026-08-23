# Operations Runbook

Monitor health/latency/errors, source completeness, duplicates, unmatched/discount/amount-variance rates, calculation mismatches, material/negative cases, exception age, approval failures, protected-action attempts, rule/form version and audit persistence.

For incidents: stop affected ingestion/reconciliation; preserve reports, bank evidence and logs; notify revenue, treasury, accounting, tax where relevant, security/privacy and technology owners; prevent transfer/refund/ledger use; revert to approved manual reconciliation; reconcile affected periods; remediate and independently validate; obtain release approval and restore gradually.

Rollback code/config/form rules together. Never initiate or replay a financial transaction from analytical logs.
