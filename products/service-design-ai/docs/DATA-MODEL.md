# Data model

Core objects are Service, AssessmentCase, InstitutionalStakeholder, JourneyStage, BlueprintLayer, EvidenceItem, MethodSession, Deliverable, RegisterEntry, GateEvaluation, HumanDecision, RiskControl, BenefitMeasure and ReportVersion. IDs are stable; evidence and decisions are append-only in production. Every generated artifact records case/config/model/prompt versions, evidence references and audit digest. Production schemas require owner-approved classification, retention and field-level access rules.
