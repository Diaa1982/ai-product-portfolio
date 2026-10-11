# Product Growth Agent — Architecture

## 1. Architectural intent

The Product Growth Agent (PGA) is a governed decision-and-orchestration service for sustainable product growth. It is not a single-purpose marketing bot. It combines growth strategy, behavioral analytics, unit economics, experimentation, decision control, and multi-agent coordination.

The reference architecture separates five concerns:

1. **Experience / request layer** — receives leadership, analyst, event-driven, or agent-to-agent requests.
2. **Agent reasoning layer** — frames the decision, diagnoses the growth system, develops hypotheses, and prioritizes interventions.
3. **Tool and data layer** — GA4, Mixpanel, warehouse, CRM, billing, experimentation, campaign, and product systems.
4. **Control layer** — identity, approvals, privacy, budget thresholds, experiment governance, and immutable audit evidence.
5. **Collaboration layer** — structured handoffs to Product, Marketing, Sales, Data, Finance, and CRM/Lifecycle agents.

## 2. Logical architecture

```text
Users / Executives / Schedulers / Other Agents
                    |
                    v
             API / A2A Gateway
                    |
                    v
          Product Growth Agent Core
  +-----------------------------------------+
  | Decision Frame                          |
  | Growth Diagnosis                       |
  | Segmentation & Opportunity Detection    |
  | Hypothesis & Experiment Design          |
  | Prioritization                          |
  | Economics & Guardrail Evaluation        |
  | Decision / Recommendation Synthesis     |
  +-----------------------------------------+
      |              |                 |
      v              v                 v
 Analytics       Business Data      Agent Bus
 GA4             CRM                Product
 Mixpanel        Billing            Marketing
 Warehouse       Revenue            Sales
                 Finance            Data
                                    Finance
                                    CRM/Lifecycle
      \              |                 /
       +-------------+----------------+
                     |
                     v
             Governance Plane
     IAM | Approval | Audit | Privacy
      Budget | Experiment | Rollback
```

## 3. Control plane

The control plane is implemented through:

- `policies/guardrails.yaml` — approval and risk constraints.
- `tools/tool_registry.yaml` — tool authority and read/write classification.
- `schemas/*.json` — task, result, context, and agent-to-agent contracts.
- `workflows/growth_cycle.yaml` — governed lifecycle.
- `prompts/system_prompt.md` — behavioral and reasoning policy.

Production deployment must externalize secrets and approvals into enterprise-grade services. The YAML files define policy intent; they are not a substitute for IAM, API authorization, or transaction controls.

## 4. State and memory

### Short-term state
- current task and objective;
- current evidence bundle;
- pending tool calls;
- pending agent handoffs;
- unresolved assumptions;
- approval state.

### Long-term governed memory
- metric dictionary;
- growth model;
- segment definitions;
- experiment ledger;
- validated/rejected learnings;
- channel economics;
- product constraints;
- approval history.

Long-term memory should be implemented using a governed database or knowledge layer with versioning and access control. Chat history alone is insufficient.

## 5. Decision boundary

The PGA is autonomous for read-only analysis and proposal generation. Consequential actions are approval-gated by default. This includes production experiments, paid-media budget changes, campaign launch, customer communications, pricing, discounts, entitlements, billing, and identifiable-customer exports.

## 6. Non-functional requirements

Production implementation should provide:

- least-privilege workload identity;
- encryption in transit and at rest;
- centralized secrets management;
- immutable or tamper-evident audit records;
- idempotent write adapters;
- observability for prompts, tools, latency, cost, and errors;
- model and prompt versioning;
- rate limits and circuit breakers;
- data-quality checks;
- rollback procedures;
- offline and online evaluations;
- business continuity and incident handling.
