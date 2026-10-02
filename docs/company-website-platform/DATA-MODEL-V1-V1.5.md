# V1 / V1.5 Data Model

## Principles
Separate methodology, customer evidence, deterministic calculations and AI interpretation. Published assessment versions are immutable. Tenant-owned data carries tenant_id explicitly. Findings/recommendations retain evidence lineage. Published reports preserve snapshots. AI executions record model/prompt/agent versions.

## Global methodology entities
- assessment: id, code, slug, name, description, assessment_type, status, current_version_id, timestamps
- assessment_version: id, assessment_id, version_number, status, effective dates, methodology_notes, scoring_version, creation/approval/publication metadata
- assessment_domain: id, assessment_version_id, code, name, description, weight, display_order, minimum_completion_pct, metadata
- assessment_question: id, assessment_version_id, domain_id, question_code, question_text, help_text, question_type, required, weight, display_order, evidence flags, metadata
- question_option: id, question_id, option_code, label, description, raw_score, display_order
- scoring_rule: id, assessment_version_id, rule_code, scope_type/id, rule_type, configuration, rule_version, effective_from, created_at

## Tenant boundary
Tenant → Organizations → Memberships/Users → Runs/Results/Evidence/Findings/Recommendations/Reports.

- tenant: id, tenant_code, name, status, subscription_tier, default_locale, data_region, settings, timestamps
- organization: id, tenant_id, parent_organization_id, name, legal_name, type, industry, country_code, employee_band, website, locale, status, metadata, timestamps
- user: id, email, display_name, locale, identity provider/external ID, status, timestamps
- organization_membership: id, tenant_id, organization_id, user_id, role, status, joined_at

## V1 transaction entities
- assessment_run: id, tenant_id, organization_id, assessment_id/version_id, initiated_by, run_type, status, timestamps, completion_pct, context_snapshot
- assessment_response: id, tenant_id, run_id, question_id, response_value/text, answered_by/at, confidence, comment, timestamps
- assessment_result: id, tenant_id, run_id, assessment_version_id, scoring_version, overall_score, maturity_level, completion_pct, calculated_at, calculation_hash, status
- domain_result: id, tenant_id, result_id, domain_id, raw/normalized score, maturity_level, counts, confidence_indicator
- result_snapshot: id, tenant_id, run_id, result_id, snapshot_version, snapshot_data, generated_at

## V1.5 evidence
- evidence: id, tenant_id, organization_id, run_id, title, description, type, classification, source, filename, mime_type, storage_key, checksum, size, uploader/time, processing_status, current_version_id, metadata
- evidence_version: id, tenant_id, evidence_id, version_number, storage_key, checksum, mime_type, size, uploader, created_at, supersedes_version_id, processing_status
- evidence_extraction: id, tenant_id, evidence_version_id, extractor/version, status, extracted_text_location, structured_data, page_count, language, processed_at, errors
- evidence_chunk: id, tenant_id, extraction_id, chunk_index, page_number, section, content, embedding_reference, token_count
- evidence_link: id, tenant_id, evidence/version_id, target_type/id, relationship_type, created_by/at

## Findings and recommendations
- finding: id, tenant_id, organization_id, run_id, code, domain, title, description, type, severity, confidence, source_type, generation_method, status, creator metadata, model/prompt versions, review metadata, supersedes_finding_id, version_number
- finding_evidence: id, tenant_id, finding_id, evidence_version_id, chunk_id, relationship, citation_text, page_number, confidence, created_at
- recommendation: id, tenant_id, organization_id, code, title, description, type, priority, impact, effort, horizon, rationale, generation_method, status, creator metadata, model/prompt versions, review metadata, versioning
- recommendation_finding: tenant_id, recommendation_id, finding_id, relationship_strength, rationale
- review: id, tenant_id, target_type/id, review_type, decision, reviewer_id, comment, previous_value, approved_value, created_at

## Reporting
- report: id, tenant_id, organization_id, run_id, type, title, description, status, current_version_id, created_by, timestamps
- report_version: id, tenant_id, report_id, version_number, result_id, content_snapshot, generator metadata, model/prompt versions, PDF storage/checksum, status, approval/publication metadata
- report_item: id, tenant_id, report_version_id, item_type/id, section_code, display_order, snapshot_data

## AI and audit
- ai_execution: id, tenant_id, organization_id, execution_type, agent code/version, model provider/name/version, prompt template/version, input reference, retrieval hash, timestamps, status, token usage/cost, output reference, error code
- audit_event: id, tenant_id, organization_id, actor type/id, action, entity type/id, previous/new state hashes, metadata, timestamp

## Isolation
All tenant-owned tables carry tenant_id NOT NULL and should use PostgreSQL RLS or equivalent server-side isolation. Do not rely on UI filtering.

## V1 minimum physical model
tenants, organizations, users, organization_memberships, assessments, assessment_versions, assessment_domains, assessment_questions, question_options, scoring_rules, assessment_runs, assessment_responses, assessment_results, domain_results, result_snapshots, leads, consents, audit_events.

## V1.5 additions
evidence, evidence_versions, evidence_extractions, evidence_chunks, evidence_links, findings, finding_evidence, recommendations, recommendation_findings, reviews, reports, report_versions, report_items, ai_executions.
