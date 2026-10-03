export const scale=[["1","Ad hoc"],["2","Emerging"],["3","Defined"],["4","Managed"],["5","Optimized"]] as const;
export const questions=[
["Strategy & Execution","STR-01","Strategic objectives are clearly defined, measurable and translated into owned initiatives."],["Strategy & Execution","STR-02","Leadership routinely reviews strategic progress, dependencies and corrective actions."],
["Governance","GOV-01","Decision rights, accountability and escalation paths are clearly defined."],["Governance","GOV-02","Material risks and controls are reviewed using current evidence."],
["Performance","PER-01","KPIs have clear definitions, owners, targets and reliable data sources."],["Performance","PER-02","Performance reviews identify drivers, decisions and follow-up actions rather than only reporting status."],
["Processes","PRO-01","Critical end-to-end processes are documented with clear ownership and controls."],["Processes","PRO-02","Process performance, bottlenecks, handoffs and automation opportunities are systematically analyzed."],
["Services","SER-01","Services have defined owners, beneficiaries, outcomes, service levels and performance measures."],["Services","SER-02","Service performance and experience insights drive prioritized improvements."],
["Organization & People","ORG-01","Roles, accountabilities, capacity and competencies are aligned to priority outcomes."],["Organization & People","ORG-02","Workload and productivity information informs operating-model and workforce decisions."],
["Data & Digital","DIG-01","Core management information is accessible, reliable and connected across relevant systems."],["Data & Digital","DIG-02","Digital investments are prioritized against capabilities, processes and measurable outcomes."],
["AI Readiness","AIR-01","High-value AI use cases have clear owners, data requirements and success measures."],["AI Readiness","AIR-02","AI use is governed through human oversight, access controls, traceability, security and risk management."]
] as const;
export const domainOrder=["Strategy & Execution","Governance","Performance","Processes","Services","Organization & People","Data & Digital","AI Readiness"] as const;