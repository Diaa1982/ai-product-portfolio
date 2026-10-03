# Diagnostic Runtime V1

Flow: assessment -> engagement -> evidence storage -> extraction -> Evidence & Quality -> specialist agents -> structured findings -> Executive Synthesis -> human decision -> controlled report.

## Existing-agent mapping

| Role | Reusable assets | Reuse now | Still required |
|---|---|---|---|
| Evidence & Quality | shared evidence schema; P03/P04 provenance; P06 evidence concepts | IDs, hashes, provenance and evidence gates | malware/DLP, stronger sufficiency/conflict checks |
| Process | P10 Enterprise Process Intelligence; P06 Process Audit AI | hierarchy, traceability, maturity evidence, exceptions, audit concepts | evidence-to-canonical-process adapter; bottleneck/handoff/workload analysis |
| Performance | P09 Corporate Performance Review | KPI validation, deterministic score, variance, trend, evidence refs, approval roles | multi-KPI adapter and cross-KPI/root-cause synthesis |
| Governance/Risk/Control | P14 Control Tower; shared approvals; P01/P02 controls | risk tiers, controls, human gates, protected actions and SoD patterns | general enterprise GRC engine and policy/control extraction |
| Executive Synthesis | P01 orchestration; P02 fact/calculation/risk separation | controlled orchestration and evidence-linked output patterns | cross-domain reconciliation, contradiction/root-cause/dependency model |
| Human Review | PortfolioEngine; approval schema; P09/P14 approvals | approve/reject/return, role checks and audit chain | explicit modify/version history and reviewer UI |
| Report | structured product outputs | facts/findings/recommendations patterns | diagnostic report schema, HTML/PDF renderer, evidence appendix and publication gate |

## Execution rule
The generic SpecialistAgent is a routing/sufficiency adapter, not a replacement for P10/P09/P14. Extracted evidence should be normalized into deterministic engines wherever their contracts apply. Unsupported conclusions remain draft.

## Production gates
Before external client use: authenticated tenant identity, tenant isolation, encrypted persistent object storage, malware scanning, content-based file validation, DLP/redaction, retention/deletion, secrets management, rate limiting, immutable audit export, backup/recovery and security/privacy approval.
