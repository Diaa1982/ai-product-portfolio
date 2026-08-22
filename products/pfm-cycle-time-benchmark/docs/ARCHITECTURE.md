# Architecture

P17 uses FastAPI, a deterministic benchmark engine, versioned JSON rules, synthetic fixtures and the shared portfolio audit platform. Inputs are process observations, benchmark register, source library and assumptions. Outputs are process comparisons, QA queues, decision package and digest.

No process-mining, workflow, ERP or external benchmark connector is implemented. Future adapters must be read-only first, preserve event lineage and use canonical process IDs.
