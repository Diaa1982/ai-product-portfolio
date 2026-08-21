# Control, Risk and Governance Matrix

| Risk | Preventive control | Detective evidence | Human accountability |
|---|---|---|---|
| Invalid or incomplete source data | Required validation and evidence references | Validation issues and source reference | Data owner/process owner |
| Unauthorized agent handoff | Allow-listed transitions and success criteria | `BLOCKED` workflow event | PFM process owner |
| Budget or liquidity pressure missed | Reproducible thresholds and calculations | Alert list and metric payload | Budget/treasury authority |
| Autonomous protected action | Deny-list action check and explicit product boundary | `DENY_AUTONOMOUS_EXECUTION` result | Applicable authorized official |
| High-risk output used without review | Mandatory approval interruption | Approval reference and decision log | Configured authority |
| Segregation-of-duties conflict | Separate preparer, reviewer and authority mappings | Access and approval logs | Control owner |
| Unsupported accounting conclusion | Exception-only IPSAS-oriented review | Policy/evidence citation and accounting review | Accounting authority |
| Audit independence impaired | No audit opinion or finding closure capability | Audit follow-up status only | Audit authority |
| Silent configuration change | Versioned config, tests and change approval | Git history, CI and release record | Product/control owner |
| Sensitive data exposure | Minimize fields, access control, encryption and retention | Security logs and privacy review | Data protection/security owner |

PEFA and IPSAS references are alignment lenses, not certifications. Applicable requirements must be selected by qualified officials for the implementing jurisdiction and entity.
