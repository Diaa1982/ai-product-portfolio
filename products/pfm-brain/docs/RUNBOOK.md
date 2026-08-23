# Operations Runbook

Monitor health, latency/errors, load-sequence failures, invalid references, missing evidence, duplicates, reconciliation mismatches, high risks, SoD/authority exceptions, critical/protected actions, approval interruptions, configuration/model versions and audit persistence.

For an incident: stop affected ingestion/analysis; preserve evidence; notify product, PFM process, data, security/privacy and relevant control owners; prevent downstream use; revert to approved manual processes; reconcile against authoritative systems; investigate data/config/code/model changes; remediate and independently verify; obtain release approval; restore gradually.

Rollback the application and configuration as an approved pair. Never replay or create financial transactions from analytical logs. A safe shutdown must leave official systems and manual controls available.
