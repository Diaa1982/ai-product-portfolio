# Architecture

Candidate flow: API/UI → deterministic source/evidence verifier → version-change detector → materiality/confidence scoring → review/publication routing. P04 outputs candidate signals to P03; P03 performs broader interpretation, portfolio synthesis and executive packaging.

Production target uses orchestrated fetch/API/RSS/PDF/OCR workers, raw immutable object storage, normalized/versioned evidence, extraction/classification services, deterministic verification, scoring, analyst queue, approval service, delivery adapters and immutable audit. Persistent workflow state, RBAC, scheduled runs, egress allowlisting, observability and retry/dead-letter handling are mandatory.

Identity, audit, source or evidence-storage failure must block publication and financial action.
