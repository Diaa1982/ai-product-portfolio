# Astra Agent Observatory Frontend

Interactive reference frontend for PFM Agentic AI.

## Run

From this directory:

```bash
python -m http.server 8088
```

Open `http://localhost:8088`.

No build step or package installation is required.

## Functional interactions

- Navigate Command Center, Agents, Reports and Configuration.
- Run a synthetic fiscal pulse.
- Inspect every agent and its activity/sub-agents.
- Filter agents by domain/status.
- Create custom agents.
- Edit mandates, automation level, approval thresholds and enablement.
- Add/remove sub-agents.
- Generate variable fiscal reports using entity, mandate, period and report-type controls.
- Persist configuration locally in the browser.

## Production adapter contract

Replace the browser state adapter with authenticated services for:

- `GET /api/v1/agents`
- `POST /api/v1/agents`
- `PATCH /api/v1/agents/{id}`
- `GET /api/v1/agents/{id}/runs`
- `GET /api/v1/runs/{run_id}/events`
- `POST /api/v1/reports/generate`
- `POST /api/v1/approvals/{id}/decision`
- `GET /api/v1/fiscal-health`
- event stream `/api/v1/events/stream`

Production data must come from governed PFM source systems and an auditable event/evidence store. The included values are synthetic and are not government financial data.
