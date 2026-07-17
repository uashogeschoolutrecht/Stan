# Tasks: Azure DevOps MCP Wiki Access

**Input**: Design documents from `/specs/003-mcp-wiki-access/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL — no test tasks are generated unless explicitly requested in the spec. Manual validation scenarios from quickstart.md serve as acceptance checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- `[X]` = already completed during plan phase

## Path Conventions

- **Documentation repo**: All artifacts under `specs/003-mcp-wiki-access/`
- **Existing files affected**: `.github/copilot-instructions.md`, `docs/stan-agent/devops-access.md`

---

## Phase 1: Setup — Validation Scaffolding

**Purpose**: Create the validation folder and templates for manual scenario testing

- [X] T001 Create validation folder and README in `specs/003-mcp-wiki-access/validation/README.md` with folder purpose, file listing, and link to quickstart.md
- [X] T002 Create manual run log template in `specs/003-mcp-wiki-access/validation/quickstart-run.md` with scenario columns (ID, name, result, notes, date)
- [X] T003 [P] Create link-check template in `specs/003-mcp-wiki-access/validation/link-check.md` with all internal/external links from feature artifacts

---

## Phase 2: Foundational — Shared Artifacts

**Purpose**: Core design documents that MUST be in place before any user story implementation

**⚠️ CRITICAL**: All Phase 2 tasks are already completed during the plan phase. Remaining work is verification.

- [X] T004 Consolidate MCP wiki-read behavior contract in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — includes transport mechanism, MCP tool mapping, MCP error mapping, source anchoring rules, configuration reference, and 8 acceptance test vectors
- [X] T005 Define MCP error-to-outcome mapping in `specs/003-mcp-wiki-access/research.md` — Decision 5 maps 5 MCP failure modes to contract outcomes (success, not_found, no_content, unavailable, access_denied)
- [X] T006 [P] Add MCP-specific entities to data model in `specs/003-mcp-wiki-access/data-model.md` — MCPConnectionConfig entity with configFile, domains, deploymentMode, authMethod, configuredTools; WikiAccessResult includes mcpToolUsed field
- [X] T007 [P] Add FR-to-quickstart traceability map in `specs/003-mcp-wiki-access/quickstart.md` — all 11 FRs mapped to 9 scenarios (S1–S9)
- [X] T008 Capture MCP non-regression guardrail in `specs/003-mcp-wiki-access/plan.md` — Constitution Check shows all 6 articles passing; quarterly strategy behavior preserved

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Answer Wiki Questions Through MCP (Priority: P1) 🎯 MVP

**Goal**: Stan answers wiki questions using MCP Server tools (topic-based and page-specific retrieval)

**Independent Test**: Ask Stan a known wiki topic; verify response uses current wiki content obtained through MCP Server (not REST). Verify FR-001, FR-002, FR-003.

### Implementation (already completed during plan phase)

- [X] T009 [US1] Add topic-based MCP retrieval rules to contract in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — topic-style prompts resolved via `mcp_ado_search_wiki` or `wiki get_page`/`wiki get_page_content`
- [X] T010 [US1] Add page-specific MCP retrieval rules to contract in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — explicit page hints use `wiki get_page` + `wiki get_page_content`; response must stay consistent with page content
- [X] T011 [P] [US1] Add MCP tool mapping table in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — 6 tools mapped (list_wikis, get_wiki, list_pages, get_page, get_page_content, mcp_ado_search_wiki)
- [X] T012 [US1] Document MCP discovery-to-retrieval flow in data model in `specs/003-mcp-wiki-access/data-model.md` — UserQuery triggers MCP tool calls via MCPConnectionConfig; WikiAccessResult captures tool used and outcome

### Validation

- [X] T013 [US1] Add US1 validation procedure in `specs/003-mcp-wiki-access/validation/us1-results.md` — structured log for scenarios S1 (topic retrieval), S2 (page retrieval) with pass/fail fields linked to FR-001, FR-002, FR-003

**Checkpoint**: User Story 1 fully functional — MVP candidate

---

## Phase 4: User Story 2 — Faster and More Accurate Wiki-Backed Answers (Priority: P2)

**Goal**: Stan's wiki responses are faster (via MCP) and correctly scoped to wiki-only content

**Independent Test**: Ask a wiki-backed question; verify source attribution is provided and non-wiki scopes are rejected. Compare response correctness.

### Implementation (already completed during plan phase)

- [X] T014 [US2] Add source attribution rules for MCP in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — must mention Data Science Pool Azure DevOps wiki; include page title/path when available
- [X] T015 [US2] Add out-of-scope MCP guardrails in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — non-wiki scope-limit response; redirect to wiki-specific questions
- [X] T016 [P] [US2] Add source transparency scenario to quickstart in `specs/003-mcp-wiki-access/quickstart.md` — S3 covers source identification after wiki-derived answer
- [X] T017 [P] [US2] Add out-of-scope scenario to quickstart in `specs/003-mcp-wiki-access/quickstart.md` — S4 covers non-wiki content requests

### Validation

- [X] T018 [US2] Add US2 validation procedure in `specs/003-mcp-wiki-access/validation/us2-results.md` — structured log for scenarios S3 (source transparency), S4 (out-of-scope), S7 (follow-up), S8 (no regression) with pass/fail fields linked to FR-004, FR-005, FR-009, FR-010

**Checkpoint**: User Stories 1 AND 2 functional and independently testable

---

## Phase 5: User Story 3 — Fail Clearly When DevOps Connection Is Unavailable (Priority: P3)

**Goal**: Stan returns clear, deterministic messages for unavailable, restricted, not-found, and no-content wiki scenarios

**Independent Test**: Simulate unavailable/restricted/not-found conditions; verify Stan returns the correct user-facing message per contract outcome matrix.

### Implementation (already completed during plan phase)

- [X] T019 [US3] Add MCP unavailability response behavior in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — unavailable outcome with retry guidance; must not present stale content
- [X] T020 [US3] Add MCP access-restricted response behavior in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — access_denied outcome with request-access suggestion; must avoid implying missing page
- [X] T021 [US3] Add not-found/no-content response behavior in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` — not_found outcome with topic refinement; no_content outcome with adjacent page suggestion
- [X] T022 [P] [US3] Add failure simulation scenarios to quickstart in `specs/003-mcp-wiki-access/quickstart.md` — S5 (unavailability), S6 (access restriction), S7 (not-found/follow-up)

### Validation

- [X] T023 [US3] Add US3 validation procedure in `specs/003-mcp-wiki-access/validation/us3-results.md` — structured log for scenarios S5 (unavailability), S6 (access restriction), S7 (not-found) with pass/fail fields linked to FR-006, FR-007, FR-008, SC-003

**Checkpoint**: All user stories functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Remove REST wiki-read code, update repo instruction files, and final validation

- [X] T024 [P] Update `.github/copilot-instructions.md` to reference 003 contract path — change `specs/002-read-devops-wiki/contracts/wiki-read-contract.md` to `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` (FR-011)
- [X] T025 [P] Rewrite `docs/stan-agent/devops-access.md` for MCP Server — replace REST API documentation with MCP server setup (Remote/HTTP + Local/stdio options), configuration JSON examples, domain filtering guidance, and authentication notes (FR-011)
- [X] T026 [P] Update `README.md` specs listing — add `003 — MCP Wiki Access` reference alongside existing 001 and 002 entries (Article IV)
- [X] T027 [P] Run full quickstart execution log in `specs/003-mcp-wiki-access/validation/quickstart-run.md` — waived by user on 2026-07-17; manual MCP validation not executed
- [X] T028 [P] Verify all feature links and references in `specs/003-mcp-wiki-access/validation/link-check.md` — waived by user on 2026-07-17; full manual link verification not executed
- [X] T029 Map completed evidence to success criteria in `specs/003-mcp-wiki-access/validation/final-report.md` — document how SC-001 (≥90% known topics), SC-002 (≥95% source match), SC-003 (100% error handling) are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Already completed during plan phase
- **User Stories (Phase 3–5)**: Implementation tasks are already done; validation tasks depend on Phase 1 (validation folder exists)
- **Polish (Phase 6)**: Depends on all validation procedures existing (T013, T018, T023) and Phase 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Independent — no dependencies on other stories
- **User Story 2 (P2)**: Independent — can proceed without US1
- **User Story 3 (P3)**: Independent — can proceed without US1/US2

### Within Each User Story

- Implementation tasks are already [X] (completed during plan)
- Validation procedures depend on Phase 1 (validation folder exists)

### Parallel Opportunities

- All Setup tasks marked [P] (T003) can run in parallel
- All validation tasks (T013, T018, T023) can run in parallel once Phase 1 is done
- All Polish tasks marked [P] (T024, T025, T026, T027) can run in parallel
- T024 (copilot-instructions.md), T025 (devops-access.md), and T026 (README.md) modify different files — fully parallel

---

## Parallel Example: User Story 1

```bash
# Validation procedures can be created in parallel:
Task: "Create US1 validation procedure in validation/us1-results.md"
Task: "Create US2 validation procedure in validation/us2-results.md"
Task: "Create US3 validation procedure in validation/us3-results.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (validation scaffolding) — ~3 tasks
2. Phase 2: Already done — skip
3. Phase 3: US1 validation — T013
4. **STOP and VALIDATE**: Run S1, S2 to verify US1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + validation scaffolding → ready for manual testing
2. Validate US1 → MVP ready (wiki answers via MCP)
3. Validate US2 → source transparency and accuracy verified
4. Validate US3 → failure handling verified
5. Polish: remove REST code, update instruction files, final sign-off

### Parallel Team Strategy

1. Developer A: Phase 1 (all 3 setup tasks)
2. Once Phase 1 done, parallel:
   - Developer A: Phase 3 validation (T013)
   - Developer B: Phase 4 validation (T018)
   - Developer C: Phase 5 validation (T023)
3. Polish tasks (T024, T025, T026, T027) can be parallelized across team after all validation procedures are in place

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Tasks marked [X] were completed during the plan phase (design artifacts)
- Each user story should be independently completable and testable
- S9 (REST code removal) is validated in Phase 6 via T024 and T025
- S10 (not-found/no-content) is validated in Phase 5 via T023
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

## Phase 7: Convergence

- [X] T030 Add explicit VS Code MCP setup and connection activation steps to `docs/stan-agent/devops-access.md` and align `specs/003-mcp-wiki-access/quickstart.md` prerequisites with that documented flow per `plan: MCP server configuration` (partial)
- [ ] T031 Reconcile scenario counts, scenario references, and story wording across `specs/003-mcp-wiki-access/quickstart.md`, `specs/003-mcp-wiki-access/tasks.md`, and `specs/003-mcp-wiki-access/validation/final-report.md` so all artifacts consistently reflect S1-S10 and the current P2 accuracy-focused scope per `SC-003` and `plan: manual validation approach` (contradicts)
- [ ] T032 Record the confirmed live wiki-backed smoke test in `specs/003-mcp-wiki-access/validation/quickstart-run.md` and update `specs/003-mcp-wiki-access/validation/final-report.md` to distinguish executed evidence from waived scenarios per `SC-001` and `SC-002` (partial)
