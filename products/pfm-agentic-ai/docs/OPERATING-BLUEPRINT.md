# PFM Operating Blueprint

## Operating model

P01 sits above existing source systems as an analytical and controlled-workflow layer. Any FMIS, budget, treasury, revenue, debt or audit connection is an implementation assumption until its owner, interface, data contract, security controls and legal basis are validated.

The nine agents cover fiscal strategy, budget preparation, budget execution/commitments, revenue, treasury/cash, debt/fiscal risk, accounting/reporting, internal control/audit follow-up, and performance/executive reporting. They do not replace accountable officials.

## Decision rights

- AI may validate structured inputs, calculate approved formulas, classify configured risks, assemble evidence and draft recommendations.
- A process owner confirms the use case, agent card, data contract, decision rights and success measures.
- The configured human authority reviews high-risk outputs and every protected action.
- A downstream agent starts only when validation passes, the transition is allowed and required approval evidence exists.
- Audit and control functions retain independence; the system cannot issue opinions or close findings.

## Minimum control cycle

1. Register case, owner, outcome and workflow type.
2. Validate source, period, completeness, balance logic and evidence reference.
3. Run deterministic calculations and thresholds.
4. Separate facts, calculations, assumptions, risks and recommendations.
5. Interrupt and escalate high-risk or failed cases.
6. Record a human decision reference where required.
7. Handoff only to an allowed next agent with defined success criteria.
8. Preserve the complete audit event and monitor exceptions.

## Accountability

Before go-live, management must approve a RACI, valid delegations, segregation-of-duties rules, retention policy, incident process, model/change control and authoritative PFM definitions. No generic role in this repository creates real authority.
