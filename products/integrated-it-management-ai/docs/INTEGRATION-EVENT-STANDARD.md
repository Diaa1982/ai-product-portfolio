# Integration and Event Standard

Production connectors require approved purpose, system/data owner, schema contract, identity, classification, least-privilege service account, encryption, rate/error limits, reconciliation and retirement plan. Events require unique event ID, canonical entity ID, type, source/version, occurred/received times, correlation ID, classification, integrity hash and processing status. Consumers must be idempotent. Invalid, duplicate, late or unmatched events go to quarantine and owner review; they cannot trigger protected actions.
