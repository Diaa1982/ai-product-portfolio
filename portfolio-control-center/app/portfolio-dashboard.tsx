"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

type Project = {
  id: string; name: string; slug: string; category: string; owner: string; stage: string;
  maturity: string; dataPolicy: string; productionReady: boolean; riskLevel: string;
  gateProgress: number; technicalStatus: string; pilotWave: number; sourceUrl: string;
  documentName: string | null; financialKpi: number | null; operationalKpi: number | null;
  customerKpi: number | null; qualityKpi: number | null; innovationKpi: number | null;
  kpiPeriod: string | null; notes: string;
};

const categoryLabels: Record<string, string> = {
  "PFM Intelligence & Financial Operations": "PFM Intelligence",
  "PFM Architecture, Benchmarking & Maturity": "PFM Architecture",
  "Strategy, Performance & AI Governance": "Strategy & AI Governance",
  "Process, Service & Partnership Operations": "Process & Service",
  "Enterprise Architecture & Technology Management": "EA & Technology",
};
const categoryColors = ["#0d87a2", "#a07964", "#4f73c4", "#2a9d78", "#8856a7"];
const lifecycle = ["Discover", "Evaluate", "Prioritize", "Approve", "Develop", "Deploy", "Operate", "Retire"];

export default function PortfolioDashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tests, setTests] = useState(247);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All categories");
  const [selected, setSelected] = useState<Project | null>(null);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");

  async function load() {
    try {
      const response = await fetch("/api/projects", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Unable to load portfolio");
      setProjects(data.projects); setTests(data.portfolioTestCount);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to load portfolio"); }
    finally { setLoading(false); }
  }
  useEffect(() => {
    const controller = new AbortController();
    void fetch("/api/projects", { cache: "no-store", signal: controller.signal })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Unable to load portfolio");
        return data;
      })
      .then((data) => {
        setProjects(data.projects);
        setTests(data.portfolioTestCount);
      })
      .catch((cause) => {
        if (cause instanceof DOMException && cause.name === "AbortError") return;
        setError(cause instanceof Error ? cause.message : "Unable to load portfolio");
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, []);

  const filtered = useMemo(() => projects.filter((project) => {
    const matchesQuery = `${project.id} ${project.name} ${project.owner}`.toLowerCase().includes(query.toLowerCase());
    return matchesQuery && (category === "All categories" || project.category === category);
  }), [projects, query, category]);
  const groups = useMemo(() => Object.keys(categoryLabels).map((name, index) => ({ name, label: categoryLabels[name], count: projects.filter((p) => p.category === name).length, color: categoryColors[index] })), [projects]);
  const reported = projects.flatMap((p) => [p.financialKpi, p.operationalKpi, p.customerKpi, p.qualityKpi, p.innovationKpi]).filter((v): v is number => v !== null);
  const average = reported.length ? Math.round(reported.reduce((a, b) => a + b, 0) / reported.length) : null;
  const evidenceCoverage = projects.length ? Math.round(projects.filter((p) => p.documentName || p.sourceUrl).length / projects.length * 100) : 0;
  const productionApproved = projects.filter((p) => p.productionReady).length;

  async function submitProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setSaving(true); setError("");
    const response = await fetch("/api/projects", { method: "POST", body: new FormData(event.currentTarget) });
    const data = await response.json(); setSaving(false);
    if (!response.ok) { setError(data.error || "Upload failed"); return; }
    setUploadOpen(false); setNotice(`${data.project.name} was added for assessment.`); await load();
  }
  async function updateResults(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); if (!selected) return; setSaving(true);
    const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
    const response = await fetch(`/api/projects/${selected.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json(); setSaving(false);
    if (!response.ok) { setError(data.error || "Update failed"); return; }
    setSelected(data.project); setNotice(`Results updated for ${data.project.name}.`); await load();
  }

  return <main className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">AP</span><span><b>AI Portfolio</b><small>Control Center</small></span></div>
      <nav aria-label="Primary navigation">
        <a className="nav-item active" href="#overview"><Icon name="grid"/>Overview</a>
        <a className="nav-item" href="#portfolio"><Icon name="folder"/>Projects <span>{projects.length}</span></a>
        <a className="nav-item" href="#results"><Icon name="chart"/>Results & KPI</a>
        <a className="nav-item" href="#governance"><Icon name="shield"/>Governance</a>
      </nav>
      <div className="pilot-card"><span>Recommended pilot path</span><b>P08 → P14 → P16</b><small>Assess · Govern · Integrate</small></div>
      <div className="boundary"><span className="status-dot"/>Synthetic-only workspace<small>No production authorization</small></div>
    </aside>

    <section className="workspace">
      <header className="topbar"><div><p className="eyebrow">PORTFOLIO OPERATING VIEW</p><h1>Executive portfolio dashboard</h1><p>Evidence, lifecycle gates and balanced results across governed AI products.</p></div><button className="primary" onClick={() => setUploadOpen(true)}><Icon name="plus"/>Add project</button></header>
      {notice && <div className="notice" role="status">✓ {notice}<button onClick={() => setNotice("")} aria-label="Dismiss">×</button></div>}
      {error && <div className="error" role="alert">{error}<button onClick={() => setError("")} aria-label="Dismiss">×</button></div>}

      <section id="overview" className="kpi-grid" aria-label="Portfolio summary">
        <KpiCard label="Registered projects" value={loading ? "—" : projects.length} note="Across 5 operating groups" tone="teal" icon="folder" />
        <KpiCard label="Technical candidates" value={loading ? "—" : projects.filter((p) => p.technicalStatus === "Validated candidate").length} note={`${tests} portfolio tests passed`} tone="blue" icon="check" />
        <KpiCard label="Formal go-live" value={`${productionApproved}/${projects.length || 18}`} note="Accountable approval pending" tone="bronze" icon="shield" />
        <KpiCard label="Reported KPI result" value={average === null ? "Not reported" : `${average}%`} note={`${reported.length} reported measures`} tone="violet" icon="chart" />
      </section>

      <section id="results" className="analytics-grid">
        <article className="panel portfolio-mix"><PanelTitle title="Portfolio distribution" subtitle="Products by operating framework" /><div className="mix-body"><div className="donut" style={{background:donutGradient(groups, projects.length)}}><span><b>{projects.length}</b><small>products</small></span></div><div className="legend">{groups.map((g) => <div key={g.name}><i style={{background:g.color}}/><span>{g.label}</span><b>{g.count}</b></div>)}</div></div></article>
        <article className="panel readiness"><PanelTitle title="Readiness evidence" subtitle="Verified facts, not estimated maturity" /><div className="readiness-row"><Progress value={100} label="Technical candidate coverage" valueLabel="18 / 18" /></div><div className="readiness-row"><Progress value={evidenceCoverage} label="Repository / document evidence" valueLabel={`${evidenceCoverage}%`} /></div><div className="readiness-row"><Progress value={productionApproved / Math.max(projects.length,1) * 100} label="Formal go-live approvals" valueLabel={`${productionApproved} / ${projects.length || 18}`} warning /></div><p className="method-note">Gate progress remains unclaimed until an accountable authority records approval.</p></article>
        <article id="governance" className="panel lifecycle-panel"><PanelTitle title="Governed lifecycle" subtitle="Direct → Build → Run → Improve" /><div className="lifecycle">{lifecycle.map((step, index) => <div key={step} className={index === 4 ? "current" : ""}><span>{index + 1}</span><small>{step}</small></div>)}</div><div className="gate-note"><Icon name="shield"/><div><b>Human authority is mandatory</b><small>Financial approvals, risk acceptance, certification, external publication and go-live remain outside automated action.</small></div></div></article>
      </section>

      <section id="portfolio" className="panel table-panel">
        <div className="table-head"><PanelTitle title="Project register" subtitle="Select a project to inspect evidence and update results" /><div className="filters"><label className="search"><Icon name="search"/><input aria-label="Search projects" value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search project or owner"/></label><select aria-label="Filter category" value={category} onChange={(e)=>setCategory(e.target.value)}><option>All categories</option>{Object.keys(categoryLabels).map((c)=><option key={c}>{c}</option>)}</select></div></div>
        <div className="table-wrap"><table><thead><tr><th>Project</th><th>Group</th><th>Lifecycle</th><th>Risk</th><th>Gate evidence</th><th>Technical status</th><th></th></tr></thead><tbody>{loading ? <tr><td colSpan={7} className="empty">Loading portfolio…</td></tr> : filtered.length === 0 ? <tr><td colSpan={7} className="empty">No matching projects.</td></tr> : filtered.map((p)=><tr key={p.id} onClick={()=>setSelected(p)} tabIndex={0} onKeyDown={(e)=>{if(e.key==="Enter")setSelected(p)}}><td><div className="project-name"><span>{p.id}</span><div><b>{p.name}</b><small>Wave {p.pilotWave}</small></div></div></td><td><span className="category-pill">{categoryLabels[p.category] || p.category}</span></td><td>{p.stage}</td><td><span className={`risk ${p.riskLevel.toLowerCase().replace(" ","-")}`}>{p.riskLevel}</span></td><td><div className="mini-progress"><i style={{width:`${p.gateProgress}%`}}/></div><small>{p.gateProgress}% recorded</small></td><td><span className="validated">● {p.technicalStatus}</span></td><td><button className="icon-button" aria-label={`Open ${p.name}`}><Icon name="arrow"/></button></td></tr>)}</tbody></table></div>
      </section>
      <footer><span>AI Product Portfolio Control Center</span><span>Evidence-led · Human-accountable · Synthetic-only baseline</span></footer>
    </section>

    {uploadOpen && <Modal title="Add a project" subtitle="Register a new project and attach its initial evidence." onClose={()=>setUploadOpen(false)}><form onSubmit={submitProject} className="form-grid"><Field label="Project name"><input name="name" required maxLength={120} placeholder="e.g. Budget Forecasting Assistant"/></Field><Field label="Portfolio group"><select name="category" required defaultValue=""><option value="" disabled>Select group</option>{Object.keys(categoryLabels).map((c)=><option key={c}>{c}</option>)}</select></Field><Field label="Accountable owner"><input name="owner" maxLength={100} placeholder="Role or accountable function"/></Field><Field label="Lifecycle stage"><select name="stage" defaultValue="Discover">{lifecycle.map((s)=><option key={s}>{s}</option>)}</select></Field><Field label="Evidence document" wide><input name="document" type="file" accept=".pdf,.json,.zip,.docx,.xlsx"/><small>PDF, JSON, ZIP, DOCX or XLSX · maximum 10 MB</small></Field><Field label="Scope and notes" wide><textarea name="notes" maxLength={1000} placeholder="Purpose, public value outcome, boundary and expected result"/></Field><div className="form-boundary"><Icon name="shield"/><span>New records remain synthetic-only, not production ready and subject to formal governance gates.</span></div><div className="modal-actions"><button type="button" className="secondary" onClick={()=>setUploadOpen(false)}>Cancel</button><button className="primary" disabled={saving}>{saving ? "Adding…" : "Add for assessment"}</button></div></form></Modal>}
    {selected && <Modal title={selected.name} subtitle={`${selected.id} · ${categoryLabels[selected.category] || selected.category}`} onClose={()=>setSelected(null)} wide><div className="detail-summary"><div><small>Technical status</small><b>{selected.technicalStatus}</b></div><div><small>Data policy</small><b>{selected.dataPolicy}</b></div><div><small>Formal go-live</small><b>{selected.productionReady ? "Approved" : "Not approved"}</b></div>{selected.sourceUrl && <a href={selected.sourceUrl} target="_blank" rel="noreferrer">Open GitHub ↗</a>}</div><form onSubmit={updateResults} className="results-form"><h3>Record approved monitoring results</h3><p>Enter percentages only when a baseline, owner and evidence period are confirmed. Blank values remain “not reported”.</p><div className="five-kpis"><NumberField label="Financial / value" name="financialKpi" value={selected.financialKpi}/><NumberField label="Operational" name="operationalKpi" value={selected.operationalKpi}/><NumberField label="Customer" name="customerKpi" value={selected.customerKpi}/><NumberField label="Quality" name="qualityKpi" value={selected.qualityKpi}/><NumberField label="Innovation" name="innovationKpi" value={selected.innovationKpi}/></div><div className="form-grid compact"><Field label="Reporting period"><input name="kpiPeriod" defaultValue={selected.kpiPeriod || ""} placeholder="e.g. Q3 2026"/></Field><Field label="Lifecycle stage"><select name="stage" defaultValue={selected.stage}>{lifecycle.map((s)=><option key={s}>{s}</option>)}</select></Field><Field label="Risk classification"><select name="riskLevel" defaultValue={selected.riskLevel}>{["Not assessed","Low","Moderate","High","Critical"].map((r)=><option key={r}>{r}</option>)}</select></Field><Field label="Approved gate evidence %"><input name="gateProgress" type="number" min="0" max="100" defaultValue={selected.gateProgress}/></Field></div><div className="formal-warning"><Icon name="shield"/><span>Updating KPIs does not approve PEFA results, IPSAS compliance, audit conclusions, financial actions, residual risk or production release.</span></div><div className="modal-actions"><button type="button" className="secondary" onClick={()=>setSelected(null)}>Close</button><button className="primary" disabled={saving}>{saving ? "Saving…" : "Save results"}</button></div></form></Modal>}
  </main>;
}

function donutGradient(groups:{count:number;color:string}[],total:number){let cursor=0;return `conic-gradient(${groups.map(g=>{const start=cursor/Math.max(total,1)*100;cursor+=g.count;return `${g.color} ${start}% ${cursor/Math.max(total,1)*100}%`}).join(",")})`}
function KpiCard({label,value,note,tone,icon}:{label:string;value:string|number;note:string;tone:string;icon:string}) { return <article className={`kpi-card ${tone}`}><div><span>{label}</span><b>{value}</b><small>{note}</small></div><i><Icon name={icon}/></i></article>; }
function PanelTitle({title,subtitle}:{title:string;subtitle:string}) { return <div className="panel-title"><h2>{title}</h2><p>{subtitle}</p></div>; }
function Progress({value,label,valueLabel,warning=false}:{value:number;label:string;valueLabel:string;warning?:boolean}) { return <div className="progress"><div><span>{label}</span><b>{valueLabel}</b></div><div><i className={warning?"warning":""} style={{width:`${Math.max(0,Math.min(100,value))}%`}}/></div></div>; }
function Field({label,children,wide=false}:{label:string;children:React.ReactNode;wide?:boolean}) { return <label className={wide?"wide":""}><span>{label}</span>{children}</label>; }
function NumberField({label,name,value}:{label:string;name:string;value:number|null}) { return <label><span>{label}</span><div><input name={name} type="number" min="0" max="100" defaultValue={value ?? ""} placeholder="—"/><i>%</i></div></label>; }
function Modal({title,subtitle,onClose,children,wide=false}:{title:string;subtitle:string;onClose:()=>void;children:React.ReactNode;wide?:boolean}) { return <div className="modal-backdrop" role="presentation" onMouseDown={(e)=>{if(e.target===e.currentTarget)onClose()}}><section className={`modal ${wide?"modal-wide":""}`} role="dialog" aria-modal="true" aria-label={title}><header><div><h2>{title}</h2><p>{subtitle}</p></div><button onClick={onClose} aria-label="Close">×</button></header>{children}</section></div>; }
function Icon({name}:{name:string}) { const paths:Record<string,React.ReactNode>={grid:<><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></>,folder:<path d="M3 6h6l2 2h10v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6Z"/>,chart:<><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></>,shield:<path d="M12 2 20 5v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5l8-3Z"/>,plus:<path d="M12 5v14M5 12h14"/>,check:<path d="m4 12 5 5L20 6"/>,search:<><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></>,arrow:<path d="m9 18 6-6-6-6"/>}; return <svg viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>; }
