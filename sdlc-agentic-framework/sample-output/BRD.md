# BRD-001 — Employee Leave Management
**Traceability:** REQ-001
## Executive Summary (confidence: 0.95)
Automate a governed, auditable leave lifecycle.
## Business Objective (confidence: 0.90)
Reduce handoffs and decision errors.
## Scope (confidence: 0.90)
Submit, check balance, approve/reject, notify and audit.
## Out of Scope (confidence: 0.88)
Payroll and production identity integrations.
## Functional Requirements (confidence: 0.92)
FR-001 submit; FR-002 balance; FR-003 decide; FR-004 notify and audit.
## Non-Functional Requirements (confidence: 0.85)
Fast responses, mandatory validation, clear errors and integration seams.
## Assumptions, Constraints, Risks, Dependencies (confidence: 0.78)
Identity exists; local JSON is used; concurrent requests are a risk; employee directory is a dependency.
## Acceptance Criteria Summary (confidence: 0.90)
Valid requests become pending; invalid and duplicate requests are rejected.
