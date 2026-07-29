# Prompt Engineering Log

| Significant prompt | Purpose | Agent | Codex response summary | Refinement | Why it improved the solution |
|---|---|---|---|---|---|
| “Normalize the raw requirement; emit stable IDs for rules, NFRs, assumptions, and questions.” | Establish machine-readable intake | Intake | Extracted actors and categorized statements | Required deterministic ID prefixes and fallback values | Makes reruns predictable and downstream references stable |
| “Retrieve only mock historical context relevant to the feature.” | Ground planning locally | Context | Returned BRDs, patterns, decisions, modules, risks | Constrained retrieval to checked-in JSON | Prevents invented external dependencies |
| “Write every BRD section with a confidence score.” | Expose ambiguity | BRD | Produced scoped business document | Added out-of-scope, risks, dependencies, AC summary | Makes approval informed rather than ceremonial |
| “Decompose BRD into epic/stories; AC must be Given/When/Then.” | Create testable backlog | Story | Produced prioritized estimated stories | Added stable AC IDs and requirement references | Enables direct test/code lineage |
| “Plan implementation before generating code; map AC to code and tests.” | Enforce architecture gate | Code Plan | Produced router/service/repository plan | Added DTO, UI, data model and explicit approval | Prevents code-first drift |
| “Review code against BRD, stories, security, validation and traceability.” | Automate first-pass review | Review | Produced severity-tagged findings | Separated PoC pass checks from production gaps | Honest, demo-friendly quality signal |
| “Construct typed nodes and semantic edges from requirement to release.” | Preserve knowledge lineage | Knowledge Graph | Produced graph JSON | Added AC, review, sanity and QA nodes | Proves complete end-to-end traceability |

## Prompt pattern
Each agent prompt follows: **role → bounded inputs → required sections → stable IDs → traceability references → deterministic fallback → output schema**. This reduces ambiguity, supports validation, and permits future Ollama enhancement without changing API contracts.

## Evaluator-driven refinement log
| Evaluator concern | Refinement prompt | Result |
|---|---|---|
| Generated stub did not prove business rules | “Implement an executable leave DTO/service/repository API with approved, duplicate, balance, authorization and validation paths.” | Added SQLite-backed demo endpoints and focused service tests |
| Demo impact was difficult to see | “Expose business outcome metrics, both gate states, and a timestamped execution ledger without a chart library.” | Added four impact cards, governance panel and lightweight audit timeline |
| Artifacts were technically present but hidden | “Make checked-in sample outputs discoverable on initial load and previewable without navigation complexity.” | Added responsive artifact gallery and modal preview |
| Lineage looked like plain text | “Render typed nodes and labeled semantic edges with accessible, dependency-free React/CSS.” | Added horizontally navigable requirement-to-release visualization |
