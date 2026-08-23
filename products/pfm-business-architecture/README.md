# PFM Business Architecture

**Product ID:** P13  
**Stage:** Technical deployment candidate  
**Data policy:** Synthetic only  
**Production ready:** No

P13 translates public value, mandates and fiscal strategy into an 11-stage PFM value chain, L1 capabilities, processes, services, information, systems, KPIs, risks, controls and outcomes. It creates an evidence-led capability heatmap and draft transition roadmap without taking statutory, policy, investment or operating-model decisions.

## Executable scope

- Versioned PFM metamodel with 11 value-chain stages and 15 L1 capability domains.
- Deterministic traceability, repository-quality and missing-stage validation.
- Evidence-gated 1–5 maturity, gap analysis and transparent `criticality × gap` priority.
- Draft three-wave transition roadmap and design-authority decision package.
- PEFA-informed and IPSAS-oriented reference metadata with no compliance conclusion.
- FastAPI endpoints, browser workbench, synthetic fixture, 15 focused tests and hardened container.

Run `python -m unittest tests.test_p13_pfm_business_architecture -v`, start the API and open `/p13`.

Reference labels for GRP, Hyperion, TMS, Bayan, Power BI and ALMAS in synthetic data are patterns—not proof of connectivity. P13 is not a statutory ledger, autonomous approval system, official PEFA assessment or IPSAS certification tool.

See [the checklist](GO-LIVE-CHECKLIST.md), [PRD](docs/PRD.md), [architecture](docs/ARCHITECTURE.md), [operating cycle](docs/PFM-OPERATING-CYCLE.md), [metamodel](docs/CAPABILITY-METAMODEL.md), [scoring](docs/SCORING-METHODOLOGY.md), [API](docs/API.md) and [go-live evidence](docs/GO-LIVE-EVIDENCE.md).
