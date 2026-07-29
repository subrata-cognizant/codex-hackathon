# Field Mapping
| Raw requirement field | Normalized requirement DTO | BRD field | Story field | Code artifact | Test artifact | Release artifact |
|---|---|---|---|---|---|---|
| Raw actor | `actors` | Scope/stakeholder | `persona` | Role check boundary | Persona authorization case | QA role checklist |
| Feature action | `raw_text`, `feature_name` | Functional Requirements | Narrative/title | Router + service method | API happy path | Release notes |
| Business rule | `business_rules[].id/text` | Functional Requirements | Given/When/Then | Service validation | Duplicate/balance tests | Known limitations/checklist |
| Quality expectation | `non_functional_requirements` | NFRs | AC outcome | DTO/error contract | Response/error assertion | Deployment/QA notes |
| Unknown detail | `open_questions` | Risks/assumptions | Dependency | Adapter seam | Mock/edge case | Open risk |
| Constraint | `constraints` | Constraints | Dependency | JSON repository | Repository test | Deployment note |
| Requirement ID | `REQ-001` | Traceability header | `requirement_id` | `AC-001` comment/result | `TEST-001` | `RELEASE-001` references |
