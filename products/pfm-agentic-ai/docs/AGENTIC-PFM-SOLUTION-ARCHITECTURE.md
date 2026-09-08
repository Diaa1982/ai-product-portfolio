# Agentic PFM Solution Architecture

## 1. Purpose
PFM Agentic AI is a governed fiscal-intelligence and workflow platform spanning the public finance management cycle. It is designed to sense fiscal signals, support strategy and budgeting, monitor execution, forecast liquidity, support revenue and treasury operations, improve accounting integrity, orchestrate consolidation, and generate mandate-driven fiscal reporting.

The platform does **not** collapse preparation, approval, execution and reconciliation into one autonomous actor. Protected actions remain subject to applicable law, financial regulations, delegated authority and segregation of duties.

## 2. Closed-loop PFM operating cycle

`Signals → Strategic Direction → Fiscal Strategy → Budget Formulation → Approval → Budget Execution → Treasury & Revenue → Accounting → Consolidation → Fiscal Health → Strategy Review`

Cross-cutting control plane: `Policy | Authority | Evidence | Risk | Security | Audit | Human Approval | Agent Registry`.

## 3. Agent domains

| Domain | Primary agents | Core output |
|---|---|---|
| Strategy | Signal Intelligence; Strategic Fiscal Intelligence | evidence-backed signals, scenarios, strategic fiscal priorities |
| Budget | Budget Allocation; Budget Challenge; Budget Execution | allocations, challenge findings, execution forecasts, amendments |
| Treasury | Cash Forecasting; Funding & Transfers; Treasury & Liquidity | cash needs, controlled funding instructions, liquidity and deposit recommendations |
| Revenue | Revenue Intelligence; Revenue Reconciliation | collection intelligence, pricing/legal analysis, reconciliations, refund preparation |
| Accounting | Accounting Operations; Government Consolidation | accounting exceptions, close readiness, eliminations, draft consolidated statements |
| Intelligence | Fiscal Health | budget-cash-accrual bridge, fiscal health, risk and forecast intelligence |
| Assurance | PFM Assurance | evidence, policy, authority and segregation-of-duties checks |

## 4. Agent execution contract
Every agent should expose a common runtime envelope:

```json
{
  "run_id": "uuid",
  "agent_id": "budget-execution",
  "parent_agent_id": null,
  "trigger": {"type": "schedule|event|user|agent", "source": "..."},
  "mandate": "approved mandate version",
  "inputs": [{"source": "system", "reference": "...", "as_of": "..."}],
  "status": "queued|running|waiting_approval|completed|exception|failed",
  "steps": [],
  "findings": [],
  "recommendations": [],
  "proposed_actions": [],
  "confidence": 0.0,
  "evidence": [],
  "approval": {"required": true, "gate": "G3", "reference": null},
  "started_at": "ISO-8601",
  "completed_at": null
}
```

## 5. Maker-checker-executor-reconciler pattern
For material financial actions, the minimum interaction is:

1. **Maker agent** prepares analysis or transaction proposal.
2. **Checker/assurance agent** independently validates evidence, rules, limits and conflicts.
3. **Authorized human/system authority** approves where required.
4. **Execution agent/integration** performs the authorized instruction.
5. **Reconciliation agent** independently confirms settlement and accounting outcome.
6. **Assurance agent** records control evidence and monitors exceptions.

An agent that recommends a material financial action must not be the sole approver and reconciler of the same action.

## 6. Observability and Agents page
The frontend Agent Observatory provides:

- current status for every agent;
- current/last action;
- domain and automation level;
- confidence indicator;
- approval threshold;
- parent/sub-agent hierarchy;
- recent activity trail;
- exception and approval states;
- configurable mandate and enablement state.

Production telemetry should persist agent runs and step events in an append-only event store. WebSocket or Server-Sent Events can stream updates to the Agents page.

## 7. Configurable agents and sub-agents
Agent behavior is configuration-driven. A parent agent owns the approved business mandate; sub-agents provide bounded specialist capability. Each configurable object should contain:

- stable ID and version;
- name and domain;
- mandate;
- allowed tools and data domains;
- prohibited actions;
- automation level;
- materiality/approval thresholds;
- evidence requirements;
- escalation route;
- schedules/triggers;
- model policy;
- parent/child relationship;
- enabled/disabled state.

Adding a sub-agent must not silently expand the parent agent's legal or financial authority.

## 8. Variable report factory
Reports are generated from a common semantic fiscal model and can be filtered by:

- mandate;
- entity;
- programme/service;
- economic or administrative expenditure classification;
- approved and adjusted budget;
- commitments, obligations and actuals;
- cash paid;
- accruals;
- revenue stream;
- forecast and forecast variance;
- delayed transactions/milestones;
- fiscal risks and exceptions;
- accounting close status;
- consolidation status;
- period and comparative period.

Every generated report should carry `as-of date`, scope, source lineage, data-quality status, material assumptions, forecast method, exception count and approval/publication status.

## 9. Fiscal health model
The executive fiscal-health layer should combine six perspectives: fiscal position, budget health, cash/liquidity health, accrual health, fiscal risk and operational/accounting integrity. The index is decision support, not a substitute for statutory financial statements or formal fiscal reporting.

## 10. Frontend
`frontend/` contains a dependency-light interactive reference implementation with:

- Astra-inspired dark spatial design;
- animated fiscal-health orb and orbit system;
- live orchestration activity stream;
- agent monitoring and drill-down;
- configurable agents and sub-agents;
- mandate-driven report factory;
- browser persistence through local storage;
- responsive layout.

The reference frontend intentionally uses synthetic data. It is fully interactive in-browser but must be connected to authenticated APIs and the event store for production.

## 11. Production integration architecture
Recommended logical components:

`Source Systems → Integration/Event Layer → Fiscal Semantic Layer → Agent Runtime/Orchestrator → Policy & Authority Engine → Approval Gateway → Transaction Adapters → Evidence/Event Store → Reporting/Observability UI`

Typical source domains include budget/GRP/ERP, treasury, banking, revenue systems, payment gateways, debt, procurement, performance, strategy, risk, HR/workforce and authoritative legal/policy repositories.

## 12. Standards alignment
The implementation should be configured against the jurisdiction's binding financial legislation and policies. PEFA can structure PFM performance and control coverage; IPSAS can support applicable accrual accounting/reporting requirements; IMF GFSM can support fiscal-statistical mapping and cash/accrual analytical bridges. These frameworks do not themselves confer transaction authority.

## 13. Production definition of done
A capability is not considered production-functional until its source integrations, identity/access controls, authority rules, audit events, exception routes, approval gates, calculation tests, data-quality controls, monitoring and operational runbook are implemented and evidenced. UI-only simulations must remain labelled as synthetic/reference functionality.
