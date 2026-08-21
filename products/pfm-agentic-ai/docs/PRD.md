# Product Requirements

## Problem and outcome

PFM teams often reconcile fragmented budget, commitment, cash, accounting, control and performance evidence manually. P01 provides a traceable coordination layer that identifies exceptions early and presents validated decision support to accountable human authorities.

## Users

Budget, treasury, revenue, debt/fiscal-risk, accounting/reporting, internal-control, audit-follow-up and executive-performance teams. Organization-specific titles and delegations must be configured during implementation.

## MVP requirements

1. Configure nine functional agents and approved transitions.
2. Require business outcome, payload, success criteria, evidence and validation for each handoff.
3. Calculate available balance, utilization, commitment pressure, variance and liquidity gap reproducibly.
4. Flag variance above 20%, utilization above 95%, negative available balance, budget exceedance and negative liquidity.
5. Interrupt high-risk handoffs until a human approval reference exists.
6. Record input, output, workflow state, approval interruption, escalation and failure route.
7. Deny autonomous protected financial, legal, accounting, publication and audit actions.
8. Expose a command center and documented API using synthetic data.

## Non-goals

The MVP is not an FMIS, payment system, tax administration, accounting ledger, audit-management system, legal authority engine, or autonomous financial decision-maker. It has no live government-system integration.

## Acceptance

Automated tests pass; container starts as non-root; health/config/analyze/action-check endpoints respond; a synthetic valid case reaches `READY`; invalid evidence or transitions remain `BLOCKED`; protected actions return `DENY_AUTONOMOUS_EXECUTION`.
