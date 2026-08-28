# Delivery inventory

## Implemented capabilities

| Capability | Implementation | Enterprise outcome |
|---|---|---|
| RAG | Approved-source ingestion, chunking, Chroma retrieval, citations, offline fallback | Evidence-grounded analysis |
| Multimodal AI | Image adapter with provider-based vision analysis | Visual evidence can enter the workflow |
| Agentic AI | Tool registry, reasoning gateway, execution receipts | Agents can reason and act within controls |
| Multi-agent | Strategy, process/PFM, architecture, risk, value, synthesis roles | Cross-functional analysis and reconciliation |
| LangGraph | Stateful lifecycle, conditional approval/execution routing | Repeatable complex workflow orchestration |
| CrewAI | Delegating specialist crew alternative | Collaborative multi-agent execution option |
| MCP | Resource, tool server, discovery client | Standardized external tool integration |
| Governance | Risk score, human approval, audit logs, execution boundary | Responsible enterprise adoption |
| Interfaces | CLI, REST API, Gradio studio, Docker | Multiple consumption and deployment modes |

## Key files

- `README.md`: setup and operating instructions
- `docs/architecture.md`: reference architecture and governance cycle
- `docs/enterprise_use_cases.md`: adaptation patterns
- `config/use_cases.yaml`: domain profiles and agent/tool policies
- `config/sample_request.json`: ready-to-use enterprise example
- `src/enterprise_ai/workflow_langgraph.py`: primary governed workflow
- `src/enterprise_ai/workflow_crewai.py`: alternative CrewAI workflow
- `src/enterprise_ai/mcp_server.py`: MCP tools and resource
- `src/enterprise_ai/api.py`: FastAPI interface
- `src/enterprise_ai/ui.py`: Gradio interface
- `tests/test_core.py`: core validation tests

## Production decisions still required

1. Select enterprise model provider and hosting pattern.
2. Connect approved repositories and identity-aware retrieval.
3. Define domain-specific agents, tools, risk rules, KPIs, and approval authorities.
4. Integrate secrets, IAM, SIEM/observability, workflow approvals, and records management.
5. Complete security, privacy, legal, architecture, model, and operational assurance.
6. Pilot with representative users and evidence-based acceptance thresholds.

