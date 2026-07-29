# SDLC Agentic Framework

## Project overview
A hackathon-ready, local-first proof of concept that turns one raw feature requirement into governed, traceable SDLC artifacts. It addresses manual BA, product, engineering, QA, and release handoffs with deterministic agents, two human approval gates, and requirement-to-release lineage.

## Solution, features, and business value
Twelve focused agents normalize requirements, retrieve mock knowledge, clarify ambiguity, author a BRD, decompose work, plan sprints/code, generate a layered stub, review, validate, prepare QA handoff, and connect every artifact. Ollama is optional; deterministic templates keep demos predictable and free of external APIs. JSON provides transparent storage; the mock graph simulates institutional memory.

## Tech stack
FastAPI, Pydantic, Python, JSON; React, TypeScript, Vite; Pytest; Docker Compose. SQLite is intentionally deferred because JSON is inspectable and sufficient for a one-day PoC.

## Structure
`backend/app` contains API, agent, DTO, service, repository, core, and data layers. `frontend/src` contains API client, reusable components, and pages. `sample-output`, `postman`, `docker`, and `docs` are submission assets.

## Backend setup
```bash
cd sdlc-agentic-framework/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Open Swagger at `http://localhost:8000/docs`.

## Frontend setup
```bash
cd sdlc-agentic-framework/frontend
npm install
npm start
```
Open `http://localhost:5173` (or the URL Vite prints).

The UI derives the API host from the browser URL, so both `localhost` and
`127.0.0.1` work. Set `VITE_API_URL` only when the backend is hosted elsewhere.
If the backend is stopped, the dashboard displays the exact local API address
and startup command instead of the browser's unhelpful `Failed to fetch` error.

## API usage
```bash
curl -X POST http://localhost:8000/api/workflow/run -H 'Content-Type: application/json' -d '{"requirement_text":"Employees submit leave requests. Managers approve or reject requests. The system notifies users and maintains an audit trail."}'
curl -X POST http://localhost:8000/api/workflow/approve/brd
curl -X POST http://localhost:8000/api/workflow/approve/code-plan
curl http://localhost:8000/api/artifacts
curl http://localhost:8000/api/traceability
curl http://localhost:8000/api/demo-data
```
The first response contains `status: awaiting_brd_approval`, completed `stages`, and artifact references. Approvals advance to `awaiting_code_plan_approval` and then `complete`. Validation errors use HTTP 422; invalid/duplicate transitions use 409; missing artifacts use 404.

## Tests
```bash
cd sdlc-agentic-framework/backend
pytest
pytest --cov=app --cov-report=term-missing
```
Tests cover normalization, missing input, duplicate active requirements, approval gates, Given/When/Then mapping, approved/insufficient scenarios, generated duplicate validation, and lineage.

## Docker
```bash
cd sdlc-agentic-framework/docker
docker compose up --build
```
UI is exposed on port 3000 and API on 8000.

## Demo flow
Use **Load demo JSON** to populate intake with the checked-in sample requirement,
employees, managers, balances, leave requests, and audit trail. Run agents;
inspect/approve BRD; inspect backlog, sprint and code plan; approve
implementation; inspect generated code, review, sanity and release artifacts;
then load the lineage graph. Stop at each gate to emphasize human governance.

## Evaluator quick verification
The project includes a genuinely runnable sample feature backed by standard-library SQLite—not only generated text. Submit a request using employee `E001`, query its balance, approve it as manager `M001`, then repeat the date range to see deterministic `DUPLICATE_REQUEST` handling. Employee `E002` has two days, enabling an `INSUFFICIENT_BALANCE` example. Every response carries requirement, story, acceptance-criteria, and code references.

The dashboard immediately lists checked-in sample artifacts and, after a run, presents estimated impact, both gate states, timestamped agent audit events, artifact previews, and a semantic requirement-to-release graph. Runtime SQLite databases, dependency folders, caches, builds, and ZIP files are excluded from submission.
