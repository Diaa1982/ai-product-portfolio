export const categories = [
  "PFM Intelligence & Financial Operations",
  "PFM Architecture, Benchmarking & Maturity",
  "Strategy, Performance & AI Governance",
  "Process, Service & Partnership Operations",
  "Enterprise Architecture & Technology Management",
] as const;

const records = [
  ["P01", "PFM Agentic AI", "pfm-agentic-ai", 0],
  ["P02", "PFM Brain", "pfm-brain", 0],
  ["P03", "Strategic Radar", "strategic-radar", 2],
  ["P04", "Signal Detection Agent", "signal-detection-agent", 2],
  ["P05", "Service Design AI", "service-design-ai", 3],
  ["P06", "Process Audit AI", "process-audit-ai", 3],
  ["P07", "Partnership Management Copilot", "partnership-management-copilot", 3],
  ["P08", "AI Use Case Assessor", "ai-use-case-assessor", 2],
  ["P09", "Corporate Performance Review AI", "corporate-performance-review-ai", 2],
  ["P10", "Enterprise Process Intelligence", "enterprise-process-intelligence", 3],
  ["P11", "IPSAS Compliance AI", "ipsas-compliance-ai", 0],
  ["P12", "Revenue Reconciliation AI", "revenue-reconciliation-ai", 0],
  ["P13", "PFM Business Architecture", "pfm-business-architecture", 1],
  ["P14", "AI Governance Control Tower", "ai-governance-control-tower", 2],
  ["P15", "Enterprise Architecture Intelligence", "enterprise-architecture-intelligence", 4],
  ["P16", "Integrated IT Management AI", "integrated-it-management-ai", 4],
  ["P17", "PFM Cycle-Time Benchmark", "pfm-cycle-time-benchmark", 1],
  ["P18", "PFM Maturity & Certification", "pfm-maturity-certification", 1],
] as const;

export const seedProjects = records.map(([id, name, slug, categoryIndex]) => ({
  id, name, slug, category: categories[categoryIndex],
  owner: "Portfolio owner to confirm",
  stage: "Develop",
  maturity: "technical-deployment-candidate",
  dataPolicy: "synthetic-only",
  productionReady: false,
  riskLevel: "Not assessed",
  gateProgress: 0,
  technicalStatus: "Validated candidate",
  pilotWave: id === "P08" ? 1 : id === "P14" ? 2 : id === "P16" ? 3 : 4,
  sourceUrl: `https://github.com/Diaa1982/ai-product-portfolio/tree/main/products/${slug}`,
  notes: "Technical baseline available. Formal ownership, production data, assurance, UAT and go-live gates remain pending.",
}));
