# Service Design AI

**Product ID:** P05  
**Domain:** Institutional service lifecycle  
**Maturity:** Technical deployment candidate; not production or certification ready

Service Design AI executes an evidence-led methodology from identification and classification through design, cost-input preparation, launch readiness, operations and improvement/stop review. It produces a governed service card, five-stage journey, six-layer blueprint, method workspaces, gate assessment and end-to-end report.

## Implemented

- Exact institutional classification: no explicit request → `PUBLIC_BENEFIT`; government request → `G2G`; company/financial-institution request → `G2B`.
- Five adopted journey stages, six blueprint layers, 54 controlled deliverables and eight persistent register definitions.
- Missing-input coaching and preserved fact/assumption/AI-inference/decision labels.
- Executable three-round brainstorming, Six Thinking Hats, Five Whys and facilitated method workspaces.
- G1–G6 evidence gates with recorded human decisions and protected-action checks.
- `/p05` studio, API, 15 focused tests, synthetic fixture and hardened container.

The configured DOF profile covers institutional, G2G, G2B and public-benefit services—not direct services to individuals. AI cannot approve classification, design, cost, SLA, launch, publication or service cessation. Dubai Services 360, IDCXS, ALMAS and optional APQC mappings are locally validated alignment inputs, not certification claims.

## Run

`uvicorn src.portfolio_api.main:app --host 0.0.0.0 --port 8080`, then open `/p05`. See [Deployment](docs/DEPLOYMENT.md), [API](docs/API.md) and [UAT](docs/UAT.md).
