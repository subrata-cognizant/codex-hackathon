# API Documentation
| Method | Endpoint | Request | Success response | Errors |
|---|---|---|---|---|
| GET | `/api/health` | none | `{status, mode}` | — |
| POST | `/api/workflow/run` | `{requirement_text: string (min 10)}` | workflow state, stages, artifact references | 422 invalid; 409 duplicate active requirement |
| POST | `/api/workflow/approve/brd` | none | state awaiting code-plan approval | 409 wrong state |
| POST | `/api/workflow/approve/code-plan` | none | complete state and all references | 409 wrong state |
| GET | `/api/artifacts` | none | `{artifacts: string[]}` | — |
| GET | `/api/artifacts/{artifact_name}` | none | `{name, content}` | 404 missing/unsafe path |
| GET | `/api/traceability` | none | `{nodes, edges}` | 404 before completion |

All JSON errors use FastAPI's `{ "detail": "message" }` format. Approval request bodies are deliberately empty because a one-workflow local PoC maintains the active state in process.

## Runnable generated feature APIs
| Method | Endpoint | Request | Purpose |
|---|---|---|---|
| POST | `/api/leave/requests` | `{"employee_id":"E001","start_date":"2027-01-10","end_date":"2027-01-11","days":2,"reason":"Family event"}` | Validates balance and overlaps, persists a pending request and audit event |
| POST | `/api/leave/requests/{id}/decision` | `{"manager_id":"M001","decision":"APPROVED","comment":"Covered"}` | Enforces assigned-manager and pending-state rules |
| GET | `/api/leave/balances/E001` | none | Returns local SQLite leave balance and traceability IDs |
| GET | `/api/workflow/status` | none | Returns gate state, impact metrics, artifacts, and execution audit |
| GET | `/api/workflow/audit` | none | Returns timestamped agent and human-gate events |

### Example success
```json
{"id":"LR-A1B2C3D4","employee_id":"E001","status":"PENDING","traceability":["REQ-001","STORY-001","AC-001","CODE-001"]}
```

### Example business-rule error (HTTP 409)
```json
{"detail":{"code":"INSUFFICIENT_BALANCE","message":"Requested days exceed available leave balance"}}
```
