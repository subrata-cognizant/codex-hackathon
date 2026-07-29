# Delivery Plan

| Phase | Milestone | Done-means check |
|---|---|---|
| 1 Foundation | Layered FastAPI and JSON repository | Health API starts; DTO validation works |
| 2 Discovery | Intake/context/clarification/BRD | Stable IDs and confidence-scored BRD persisted |
| 3 Planning | Stories/sprint/code plan | Given/When/Then AC and two gates work |
| 4 Delivery | Code/review/sanity/release/lineage | Generated layered stub and complete graph exist |
| 5 Experience | React dashboard and artifact viewer | User can run, approve, browse and graph workflow |
| 6 Submission | Tests, Docker, Postman, documents | Clean checks pass and package excludes dependencies |

## Risk mitigation
- Ollama unavailable: deterministic templates remain the default.
- Demo state errors: explicit statuses and clean 409 messages.
- Scope pressure: JSON instead of production database, auth, queues, or deployment platform.
- Traceability drift: IDs are created once and reused in every downstream artifact.
- Packaging bloat: `.gitignore` excludes environments, caches, builds, dependencies and ZIPs.

## Final demo preparation
- [ ] Run backend and frontend smoke checks
- [ ] Reset sample outputs if rehearsing a clean run
- [ ] Rehearse both approval gates
- [ ] Show one negative test and lineage graph
- [ ] Keep Docker as fallback
- [ ] Verify no generated dependency directories
