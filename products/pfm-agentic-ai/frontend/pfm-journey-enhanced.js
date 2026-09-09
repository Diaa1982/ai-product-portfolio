let pfmJourneyV2=null,pfmJourneyTimer=null;
function listHtml(items,cls='logic-list'){return `<div class="${cls}">${(items||[]).map(x=>`<div>${esc(x)}</div>`).join('')}</div>`}
async function loadPFMJourney(){
  try{
    pfmJourneyV2=await fetch('/assets/pfm-journey.v2.json').then(r=>{if(!r.ok)throw new Error('journey config');return r.json()});
    renderPFMJourneyShell();showPFMStage(0);
  }catch(e){console.error(e)}
}
function renderPFMJourneyShell(){
  const section=$('#journey');if(!section||!pfmJourneyV2)return;
  let summary=$('#pfm-cycle-summary');
  if(!summary){summary=document.createElement('div');summary.id='pfm-cycle-summary';summary.className='pfm-cycle-summary panel';section.querySelector('.section-head').after(summary)}
  summary.innerHTML=`<div class="cycle-principle"><span class="tag ai">OPERATING PRINCIPLE</span><p>${esc(pfmJourneyV2.principle)}</p></div><div class="phase-band">${pfmJourneyV2.phases.map((p,i)=>`<div class="phase phase-${i+1}"><span>PHASE ${i+1}</span><b>${esc(p.name)}</b><small>Stages ${p.stages[0]}–${p.stages[p.stages.length-1]}</small></div>`).join('')}</div><div class="cycle-loop"><b>Closed loop</b><span>Final outturn, fiscal risks and data-quality evidence return to Signals & Strategy for the next planning cycle — without changing approved historical records.</span></div>`;
  const track=$('#journey-track');
  track.innerHTML=pfmJourneyV2.stages.map((s,i)=>`<button class="journey-stage v2 ${i===0?'selected':''}" data-stage="${i}" title="${esc(s.name)}"><span>${String(s.id).padStart(2,'0')}</span><b>${esc(s.short)}</b><small>${esc(s.phase)}</small></button>${i<pfmJourneyV2.stages.length-1?'<i class="journey-arrow">→</i>':'<i class="journey-arrow loop-arrow">↺</i>'}`).join('');
  $$('.journey-stage.v2').forEach(b=>b.onclick=()=>showPFMStage(+b.dataset.stage));
  const rail=document.querySelector('.control-rail');
  if(rail)rail.innerHTML=`<p class="eyebrow">PFM CONTROL PLANE</p><h3>Controls that surround every stage</h3>${[['Authority Engine','Validates delegation, role and protected action before a workflow advances.'],['Evidence Passport','Source, period, freshness, lineage, confidence, assumption and approval reference.'],['Budget Control','Original budget, approved amendments, commitments, obligations, actuals and available balance remain reconcilable.'],['Segregation of Duties','Maker ≠ checker ≠ approver ≠ executor ≠ reconciler for material actions.'],['Risk & Exception Manager','Blocks or escalates threshold breaches, missing evidence and unresolved differences.'],['Audit Event Store','Preserves input, calculation, agent output, human decision, execution reference and reconciliation result.'],['Human Approval Gateway','Appropriations, virements, releases, material journals, investments, pricing/legal decisions and final statements remain gated.']].map(x=>`<div class="control-item"><b>${x[0]}</b><span>${x[1]}</span></div>`).join('')}<div class="authority-legend"><span class="tag ai">AI: SENSE / ANALYSE / PREPARE</span><span class="tag gate">AUTHORITY: APPROVE</span><span class="tag sim">SYSTEM: RECORD / RECONCILE</span></div>`;
}
function showPFMStage(i){
  if(!pfmJourneyV2)return;const s=pfmJourneyV2.stages[i];
  $$('.journey-stage.v2').forEach((b,x)=>b.classList.toggle('selected',x===i));
  const detail=$('#journey-detail');
  const fiscalLine=buildStageFiscalLine(s.id);
  detail.innerHTML=`<div class="section-head stage-head"><div><p class="eyebrow">STAGE ${String(s.id).padStart(2,'0')} · ${esc(s.phase)}</p><h2>${esc(s.name)}</h2><p class="stage-agent">${esc(s.agent)} · <b>${esc(s.autonomy)}</b></p></div><span class="tag gate">${esc(s.gate)}</span></div>
  ${fiscalLine}
  <div class="logic-grid v2"><div><small>ACCOUNTABLE OWNER</small><strong>${esc(s.owner)}</strong></div><div><small>DECISION RIGHT</small><strong>${esc(s.authority)}</strong></div></div>
  <div class="stage-columns"><section><div class="logic-block"><b>1 · Inputs / evidence received</b>${listHtml(s.inputs)}</div><div class="logic-block"><b>2 · PFM sub-processes</b>${listHtml(s.subprocesses,'chip-list')}</div><div class="logic-block logic-engine"><b>3 · Controlled logic</b>${listHtml(s.logic,'numbered-logic')}</div></section><section><div class="logic-block calc"><b>4 · Core calculations / checks</b>${listHtml(s.calculations)}</div><div class="logic-block"><b>5 · Outputs passed forward</b>${listHtml(s.outputs)}</div><div class="logic-block evidence"><b>6 · Evidence passport</b>${listHtml(s.evidence,'chip-list')}</div></section></div>
  <div class="logic-block control"><b>7 · Controls & assurance</b>${listHtml(s.controls,'control-grid')}</div>
  <div class="authority-line"><span class="tag ai">${esc(s.autonomy)}</span><b>→</b><span class="tag gate">${esc(s.gate)}</span><b>→</b><span class="tag sim">EVIDENCE + APPROVED OUTPUT PASSES FORWARD</span></div>`;
}
function buildStageFiscalLine(id){
  if(!window.fiscal)return '<div class="stage-live-line"><span class="tag sim">SIMULATED INTERNAL</span><span>Fiscal snapshot loads from the same governed demo state.</span></div>';
  const f=window.fiscal||fiscal,t=f.totals||{},r=f.revenue||{},tr=f.treasury||{};
  const data={
    1:['Scenario',f.scenario],2:['Fiscal health',`${t.fiscal_health_index}/100`],3:['Revenue forecast',`AED ${r.forecast}B`],4:['Aggregate approved budget',`AED ${t.approved}B`],5:['Adjusted budget',`AED ${t.adjusted}B`],6:['30-day liquidity',`AED ${tr.thirty_day}B`],7:['Actual expenditure',`AED ${t.actual}B`],8:['Forecast variance',`${t.forecast_variance_percent}%`],9:['Cash paid',`AED ${t.cash_paid}B`],10:['Accrued expense',`AED ${t.accrual}B`],11:['Consolidation basis','Entity trial balances + eliminations'],12:['Final reporting status','Draft / approval required']
  };
  const pair=data[id]||['Current state','Available'];return `<div class="stage-live-line"><span class="tag sim">SIMULATED INTERNAL</span><b>${esc(pair[0])}</b><strong>${esc(pair[1])}</strong><span>· current scenario ${esc(f.scenario)}</span></div>`
}
function playPFMJourney(){
  if(!pfmJourneyV2)return;if(pfmJourneyTimer)clearInterval(pfmJourneyTimer);let i=0;showPFMStage(0);
  pfmJourneyTimer=setInterval(()=>{i++;if(i>=pfmJourneyV2.stages.length){clearInterval(pfmJourneyTimer);pfmJourneyTimer=null;return}showPFMStage(i)},1500)
}
document.addEventListener('DOMContentLoaded',()=>{
  loadPFMJourney();
  const play=$('#play-journey');if(play)play.onclick=playPFMJourney;
});
