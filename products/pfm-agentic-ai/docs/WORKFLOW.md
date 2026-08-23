# Controlled PFM Workflow

```mermaid
flowchart LR
  A[Register case and outcome] --> B[Validate data, source and evidence]
  B -->|fail| X[Remediation queue]
  B -->|pass| C[Functional agent analysis]
  C --> D[Deterministic calculations and risk classification]
  D --> E{High risk or protected action?}
  E -->|yes| F[Interrupt for authorized human decision]
  F -->|approved with reference| G{Allowed transition and success criteria?}
  F -->|rejected or returned| X
  E -->|no| G
  G -->|no| X
  G -->|yes| H[Record handoff audit event]
  H --> I[Start approved downstream agent]
  I --> J[Validated executive or operational brief]
```

## Handoff contract

Each handoff records the case/workflow, current and next agent, payload, success criteria, evidence, assumptions, input validation state, calculated output, risk, approval interruption/reference, escalation, failure route and timestamp. The next agent cannot start when the state is `BLOCKED`.

High-risk approval references demonstrate workflow authorization only; they do not by themselves prove a valid legal or financial delegation. Production integration must verify the authority system of record.
