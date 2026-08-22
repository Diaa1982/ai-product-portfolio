# Architecture

`SharePoint Partner Master + Partnership Register + Document Index → User-Initiated Copilot Review → Draft Extraction/Assessment → Strategy Employee 1 Review → Strategy Employee 2 Approval → Controlled Register Update`

Centralized metadata links records using `Partner_ID` and `Partnership_ID`; it does not require one folder per partnership. The baseline registers are Partner_Master, Partnership_Register, Document_Index, Evaluation_Cycles, Evaluation_Criteria, Utilization_Register, Lifecycle_Actions, Lists_and_Config and Copilot_Review_Log.

The GitHub reference implements deterministic application logic and API/UI testing. Microsoft 365 Copilot and SharePoint connection, permissions and data controls are production integrations—not simulated approvals or autonomous workflows.
