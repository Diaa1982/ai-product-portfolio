export const siteConfig = {
  companyName: "Transformation Intelligence",
  companyDescriptor: "Enterprise Transformation & AI Solutions",
  platformName: "Transformation Intelligence Platform",
  assessmentName: "Transformation Readiness Assessment",
  primaryCta: { label: "Start Assessment", href: "/assessments/transformation-readiness" },
  secondaryCta: { label: "Explore Platform", href: "/platform" },
  tertiaryCta: { label: "Talk to an Expert", href: "/contact" },
  navigation: [
    { label: "Solutions", href: "/solutions" },
    { label: "Platform", href: "/platform" },
    { label: "Assessments", href: "/assessments" },
    { label: "Industries", href: "/industries/government" },
    { label: "Insights", href: "/" },
    { label: "Company", href: "/company/about" },
  ],
} as const;

export const priorities = [
  ["Strategy", "Turn strategic priorities into measurable execution."],
  ["Performance", "Connect performance information to management decisions."],
  ["Processes", "Discover inefficiencies, handoffs, control gaps and automation opportunities."],
  ["Services", "Design and continuously improve customer-facing and internal services."],
  ["Governance", "Strengthen governance, risk management and internal controls."],
  ["Organization", "Improve operating models, accountability, capacity and productivity."],
  ["Digital", "Align capabilities, processes, data and technology."],
  ["AI", "Identify and implement governed, high-value enterprise AI."],
] as const;

export const solutions = [
  ["Strategy & Transformation", "Turn strategic priorities into governed programs, measurable initiatives and execution roadmaps."],
  ["Operational Excellence", "Analyze processes, operating models, workload and improvement opportunities."],
  ["Services & Experience", "Design, manage and continuously improve customer-facing and internal services."],
  ["Performance Intelligence", "Connect KPIs, initiatives, risks and operational information to improve management decisions."],
  ["Governance, Risk & Controls", "Connect governance requirements, policies, risks, controls, evidence and corrective actions."],
  ["Enterprise Architecture", "Align capabilities, services, processes, applications, data and technology with strategic priorities."],
  ["Organizational Excellence", "Understand organizational capacity, accountability, workload, competencies and productivity."],
  ["AI Transformation", "Identify, govern and implement enterprise AI use cases, agents and intelligent workflows."],
] as const;

export const agents = [
  ["Strategy Agent", "Connects objectives, KPIs, initiatives and execution."],
  ["Process Intelligence Agent", "Identifies process fragmentation, handoffs and improvement opportunities."],
  ["Service Intelligence Agent", "Analyzes service design, performance and improvement opportunities."],
  ["Performance Intelligence Agent", "Identifies trends, deviations and performance drivers."],
  ["Governance Intelligence Agent", "Analyzes governance, risk, controls and supporting evidence."],
  ["Transformation Agent", "Converts findings into structured improvement priorities and roadmaps."],
  ["Executive Intelligence", "Synthesizes cross-domain evidence to support management review and decision-making."],
] as const;
