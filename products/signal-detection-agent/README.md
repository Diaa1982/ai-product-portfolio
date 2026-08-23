# Signal Detection Agent

**Product ID:** P04  
**Release:** 1.0.0 technical deployment candidate  
**Formal go-live:** Not approved  
**Data:** Synthetic only

P04 detects evidence-grounded changes across approved regulatory, fiscal, market and operating sources. It supplies governed candidate signals to analysts and Strategic Radar; it is not a news crawler and cannot autonomously publish high-impact findings.

## Working capabilities

- Approved official sources plus controlled association/licensed-data exceptions preserving official lineage.
- Prohibited material sources: blogs, social media, general news, opinion and unverifiable aggregators.
- Current-versus-prior version/change detection with snapshot, hash, timestamps, authority, provenance token and exact citation locator.
- Evidence states: verified, pending, conflict, partial and blocked.
- Six-factor materiality and six-factor composite confidence scores.
- Priority analyst review ≥0.82; standard review 0.55–0.81; evidence enhancement <0.55; null/weak/conflicting evidence routes to analyst evidence review.
- No ordinary manual signal creation; controlled human high-impact review only.
- Separate fact, interpretation, recommendation, opportunity, risk, scenario and KPI hypothesis.
- PFM focus on execution, variance, commitments, cash, reporting, audit and systemic fiscal risk.

## Run

```bash
docker compose -f products/signal-detection-agent/deploy/docker-compose.yml up --build
```

Open `/p04`; API documentation is at `/docs`.

## Documents

[PRD](docs/PRD.md) · [Architecture](docs/ARCHITECTURE.md) · [PFM alignment](docs/PFM-ALIGNMENT.md) · [Evidence standard](docs/EVIDENCE-STANDARD.md) · [Detection method](docs/DETECTION-METHODOLOGY.md) · [Data model](docs/DATA-MODEL.md) · [API](docs/API.md) · [Security](docs/SECURITY-PRIVACY.md) · [Deployment](docs/DEPLOYMENT.md) · [Runbook](docs/RUNBOOK.md) · [Tests](docs/TEST-PLAN.md) · [UAT](docs/UAT.md) · [Go-live evidence](docs/GO-LIVE-EVIDENCE.md) · [Checklist](GO-LIVE-CHECKLIST.md)
