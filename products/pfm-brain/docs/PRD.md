# Product Requirements

## Outcome

Provide finance leadership and analysts with a reconciled, cross-domain analytical record whose evidence, calculations, limitations and decision status can be reviewed without changing authoritative financial records.

## MVP scope

1. Govern the synthetic FY2026/AED dataset and its master-before-transaction load order.
2. Validate organization, account, cost centre, period, currency, source, evidence and duplicate status.
3. Calculate budget, execution, revenue, cash, KPI, control and residual-risk measures deterministically.
4. Reconcile calculated revised budget and closing cash to expected results.
5. Check authority limits and requester/approver segregation of duties without granting approval.
6. Block missing, conflicting or unreconciled records and critical/protected actions without human approval evidence.
7. Produce separate facts, calculations, risks, assumptions and recommendations with a calculation digest.
8. Expose versioned API, workbench, tests and deployable container.

## Non-goals

No statutory reporting, official ledger, autonomous financial reasoning, transaction execution, final forecast, legal/accounting determination, or invented source-system integration. Probabilistic retrieval/generation is outside this deterministic MVP until a governed knowledge layer and evaluations are approved.

## Success criteria

All 20 acceptance themes are represented; focused tests and full portfolio CI pass; synthetic reconciled input returns `ANALYSIS_READY_FOR_HUMAN_USE`; invalid evidence/master data/SoD/reconciliation or missing critical approval returns `BLOCKED`; calculations reconcile within AED 0.01.
