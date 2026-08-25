# Owner Input Register for Pilot and Deployment

This register identifies the decisions and evidence that require accountable organizational input. Technical completion cannot substitute for these approvals.

## Immediate portfolio-level inputs

| ID | Required input or decision | Minimum evidence to provide | Supports gate |
|---|---|---|---|
| U01 | Confirm portfolio sponsor and product owners | Named sponsor and owner for P01-P18, with delegated decision rights | L0 Strategy and ownership |
| U02 | Authorize first pilot | Selected product, objectives, scope, users, dates, and approved pilot/change/review reference | L0-L1 |
| U03 | Confirm data boundary | Synthetic-only confirmation or approved non-production dataset, classification, owner, lawful use, retention, and lineage | L2 Data and evidence |
| U04 | Confirm knowledge and evaluation authority | Approved sources, rules, prompts/models, evaluation set, thresholds, versioning, and rollback owner | L3 AI and knowledge |
| U05 | Approve governance decision rights | Risk tier, excluded decisions, human review, escalation, segregation of duties, and approval authorities | L4 Governance and compliance |
| U06 | Approve security and privacy plan | IAM roles, least privilege, threat model, privacy assessment, vulnerability testing, secrets, incident owner | L5 Security and privacy |
| U07 | Approve architecture and integrations | Target hosting, environments, source and target systems, APIs, service accounts, logging, and observability | L6 Architecture and integration |
| U08 | Nominate UAT and assurance participants | User groups, scenarios, test data, thresholds, acceptance authority, and independent reviewer | L7 Verification and assurance |
| U09 | Establish operating ownership | Support model, service levels, monitoring, training, change control, continuity, backup, rollback, and evidence retention | L8-L9 |
| U10 | Approve value and release controls | KPI baselines and targets, benefit owner, residual-risk authority, formal go-live authority, and review date | L10 Authority and value |

## Minimum information requested from Diaa for the first pilot

1. Confirm **P08 - AI Use Case Assessor** as the first controlled pilot, or nominate another product with rationale.
2. Name the accountable sponsor, business product owner, technical owner, data owner, security/privacy reviewer, UAT lead, and final approval authority.
3. Provide the approved pilot, change, or review reference that must appear in GitHub evidence.
4. Confirm whether the first run remains fully synthetic. If approved non-production data will be used later, provide its classification, owner, permitted fields, retention rule, and approved storage location.
5. Confirm the intended access model. The current control center uses owner-restricted custom access.
6. Provide baseline, target, evidence source, reporting period, and accountable benefit owner for financial/value, operational, customer, quality, and innovation KPIs.

## Product-specific first inputs

| ID | Product | First accountable inputs required |
|---|---|---|
| P01 | PFM Agentic AI | Fiscal mandate, delegations, protected actions, FMIS/treasury/revenue/audit integration owners, and SoD model |
| P02 | PFM Brain | Authoritative PFM datasets, data contracts, source owners, fiscal definitions, quality thresholds, and authority matrix |
| P03 | Strategic Radar | Approved source registry, ingestion ownership, materiality thresholds, review route, and publication authority |
| P04 | Signal Detection Agent | Approved corpus, version and citation controls, confidence thresholds, high-impact review authority, and publication route |
| P05 | Service Design AI | Approved service methodology, service owners, classification rules, cost interface owner, and representative UAT services |
| P06 | Process Audit AI | Approved audit criteria, standards mappings, evidence access, assessor independence, and finding/CAPA authority |
| P07 | Partnership Management Copilot | Strategy, business, and Legal owners; register fields; Microsoft 365 permissions; DLP; reminder and escalation authority |
| P08 | AI Use Case Assessor | Assessment criteria, 60% value/40% feasibility configuration, risk route, pilot users, and approval authorities |
| P09 | Corporate Performance Review AI | KPI master, calendar, evidence owners, specialized calculation rules, corrective-action authority, and publication route |
| P10 | Enterprise Process Intelligence | Canonical process metamodel, repository owner, governance workflow, migration decision, and design authority |
| P11 | IPSAS Compliance AI | Current approved accounting guidance, expert ground truth, review thresholds, accounting authority, and secure source access |
| P12 | Revenue Reconciliation AI | Current forms, agreements, tax/accounting rules, bank and treasury sources, matching tolerances, and exception authority |
| P13 | PFM Business Architecture | Approved mandates, capability metamodel, owners, maturity method, repository, and investment/design authority |
| P14 | AI Governance Control Tower | AI policies, Board and Design Authority decision rights, risk tiers, G0-G4 approvals, assurance ownership, and residual-risk route |
| P15 | Enterprise Architecture Intelligence | Metamodel and conventions, repository owner, integration adapters, ADR authority, and security/migration gates |
| P16 | Integrated IT Management AI | ITSM/GRC/PMO/audit/ITOM/CMDB owners, thresholds, service levels, adapters, operational UAT, and release authority |
| P17 | PFM Cycle-Time Benchmark | Approved sources and licenses, event definitions, calendars, comparability rules, publication rules, and expert calibration |
| P18 | PFM Maturity & Certification | Scheme and legal authority, criteria, evidence rules, assessor competence, moderation, appeals, claims, and accreditation position |

## Evidence submission rule

Do not commit confidential government information, personal data, production financial records, credentials, internal audit evidence, or security-sensitive configurations to GitHub. Store controlled evidence only in an organization-approved repository and record a sanitized reference, owner, version, approval date, and integrity identifier in GitHub or the portfolio control center.
