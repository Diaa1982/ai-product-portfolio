# Architecture

Candidate: API/UI → deterministic risk classifier → tier controls → gate evaluator → human decision endpoint → monitoring/incident evaluator. Configuration is versioned JSON; repository data is synthetic.

Production target: enterprise identity/RBAC; portfolio, model/agent, risk/control/evidence, approval, incident and benefits stores; immutable audit; workflow orchestration; evidence object storage; policy/rule service; monitoring/event ingestion; notification/committee packs; P08 intake and delivery-product integrations; analytics and regulatory evidence exports.

All gate and monitoring services fail closed when identity, audit, policy configuration or required evidence is unavailable. Environments and decision authorities remain segregated.
