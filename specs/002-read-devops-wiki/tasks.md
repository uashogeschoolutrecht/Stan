# Tasks: Read Azure DevOps Wiki

**Input**: Design documents from `/specs/002-read-devops-wiki/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Automated tests are not explicitly requested in the specification; tasks focus on documentation and manual validation evidence.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create feature execution scaffolding and validation placeholders

- [X] T001 Create validation folder structure in specs/002-read-devops-wiki/validation/README.md
- [X] T002 Create manual run log template in specs/002-read-devops-wiki/validation/quickstart-run.md
- [X] T003 [P] Create source link-check template in specs/002-read-devops-wiki/validation/link-check.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared behavior rules that all user stories depend on

**⚠️ CRITICAL**: No user story work should begin until this phase is complete

- [X] T004 Consolidate wiki-only scope policy in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T005 Define shared retrieval outcome matrix in specs/002-read-devops-wiki/research.md
- [X] T006 [P] Define canonical entities and statuses for retrieval outcomes in specs/002-read-devops-wiki/data-model.md
- [X] T007 [P] Add traceability map from FR-001..FR-009 to validation scenarios in specs/002-read-devops-wiki/quickstart.md
- [X] T008 Capture non-regression guardrail for quarterly strategy behavior in specs/002-read-devops-wiki/plan.md

**Checkpoint**: Foundational behavior contract and validation mapping complete

---

## Phase 3: User Story 1 - Retrieve wiki information on request (Priority: P1) 🎯 MVP

**Goal**: Deliver reliable wiki topic/page retrieval response behavior

**Independent Test**: Ask for a known wiki topic and a known wiki page; response must be relevant and wiki-derived

- [X] T009 [US1] Add topic-based retrieval response rules in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T010 [US1] Add page-specific retrieval response rules in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T011 [P] [US1] Add successful retrieval examples for topic and page queries in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T012 [US1] Document follow-up context behavior for previous topic/page references in specs/002-read-devops-wiki/data-model.md
- [X] T013 [US1] Add US1 manual validation procedure and pass criteria in specs/002-read-devops-wiki/validation/us1-results.md

**Checkpoint**: User Story 1 can be validated independently as MVP

---

## Phase 4: User Story 2 - Keep responses scoped to wiki source (Priority: P2)

**Goal**: Ensure source transparency and wiki-only scope boundaries in user-visible behavior

**Independent Test**: Ask for source attribution and out-of-scope content; response must identify wiki source and scope limits

- [X] T014 [US2] Add explicit source attribution response rules in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T015 [US2] Add out-of-scope request handling guidance for non-wiki content in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T016 [P] [US2] Add source transparency validation scenario and expected outcomes in specs/002-read-devops-wiki/quickstart.md
- [X] T017 [P] [US2] Add out-of-scope validation scenario and expected outcomes in specs/002-read-devops-wiki/quickstart.md
- [X] T018 [US2] Record US2 validation evidence and results in specs/002-read-devops-wiki/validation/us2-results.md

**Checkpoint**: User Story 2 is independently testable without depending on US3

---

## Phase 5: User Story 3 - Handle access and availability issues gracefully (Priority: P3)

**Goal**: Provide deterministic, actionable error messaging for unavailable/restricted/not-found wiki requests

**Independent Test**: Simulate unavailable and restricted page requests; response must return clear remediation-oriented messages

- [X] T019 [US3] Add temporary unavailability response behavior and retry guidance in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T020 [US3] Add restricted-access response behavior and access-request guidance in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T021 [US3] Add not-found and no-content response behavior in specs/002-read-devops-wiki/contracts/wiki-read-contract.md
- [X] T022 [P] [US3] Add US3 availability/restriction/manual simulation steps in specs/002-read-devops-wiki/quickstart.md
- [X] T023 [US3] Record US3 validation evidence and results in specs/002-read-devops-wiki/validation/us3-results.md

**Checkpoint**: User Story 3 is independently testable with deterministic failure handling

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency and acceptance closure across all stories

- [X] T024 [P] Run full quickstart execution log and record outcomes in specs/002-read-devops-wiki/validation/quickstart-run.md
- [X] T025 [P] Verify all feature links and references in specs/002-read-devops-wiki/validation/link-check.md
- [X] T026 Map completed evidence to success criteria SC-001..SC-004 in specs/002-read-devops-wiki/validation/final-report.md
- [X] T027 Align top-level feature summary with final behavior contract in specs/002-read-devops-wiki/spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies, starts immediately
- **Phase 2 (Foundational)**: Depends on Phase 1, blocks all user stories
- **Phase 3 (US1)**: Depends on Phase 2, delivers MVP
- **Phase 4 (US2)**: Depends on Phase 2 and can proceed after US1 baseline is available
- **Phase 5 (US3)**: Depends on Phase 2 and can proceed in parallel with US2 if staffed
- **Phase 6 (Polish)**: Depends on all selected user stories being complete

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependency on US2 or US3
- **US2 (P2)**: Starts after Foundational; uses shared contract baseline from US1 edits
- **US3 (P3)**: Starts after Foundational; independent from US2 and focused on failure paths

---

## Phase 7: Convergence

- [ ] T028 Add wiki source-attribution instruction to `.github/copilot-instructions.md` and a wiki-response template to `docs/stan-agent/response-templates.md` so Stan cites the Data Science Pool Azure DevOps wiki (not `docs/strategy-playbook.md`) when answering wiki-backed prompts per US2/AC1, FR-002 (partial)

---

### Parallel Opportunities

- Setup tasks T003 can run with T001-T002 after validation folder exists
- Foundational tasks T006 and T007 run in parallel after T004-T005 framing
- US1 task T011 can run after T009 and T010
- US2 tasks T016 and T017 can run in parallel after T014-T015
- US3 task T022 can run in parallel with T021 after T019-T020
- Polish tasks T024 and T025 can run in parallel before T026

---

## Parallel Example: User Story 2

- Task: "T016 [US2] Add source transparency validation scenario and expected outcomes in specs/002-read-devops-wiki/quickstart.md"
- Task: "T017 [US2] Add out-of-scope validation scenario and expected outcomes in specs/002-read-devops-wiki/quickstart.md"

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate using US1 evidence in specs/002-read-devops-wiki/validation/us1-results.md

### Incremental Delivery

1. Deliver MVP (US1)
2. Add US2 for source transparency and scope control
3. Add US3 for robust access/unavailability handling
4. Run Phase 6 polish and publish final report

### Parallel Team Strategy

1. Team completes Setup + Foundational together
2. After Foundational:
   - Contributor A: US1 contract and examples
   - Contributor B: US2 transparency/scope validation
   - Contributor C: US3 failure-mode handling and validation
3. Merge in phase order and finalize evidence artifacts

---

## Notes

- [P] tasks are safe for parallel execution when listed dependencies are satisfied
- [US1]/[US2]/[US3] labels provide traceability to spec priorities
- Every story has an independent validation artifact under specs/002-read-devops-wiki/validation/
- Keep edits small and documentation-first to match repository constitution

## Phase 7: Convergence

- [X] T028 Validate restricted-page access-denied behavior and record S6 evidence in specs/002-read-devops-wiki/validation/us3-results.md per FR-006/SC-002 (missing) (waived by user request 2026-07-16)
- [X] T029 Validate known content-rich topic retrieval quality and record S1 evidence in specs/002-read-devops-wiki/validation/us1-results.md per FR-003/SC-001 (partial)
- [X] T030 Run end-to-end source transparency prompt and record S3 evidence in specs/002-read-devops-wiki/validation/us2-results.md per US2/AC1 (partial)
- [X] T031 Run end-to-end follow-up continuity check and record S7 evidence in specs/002-read-devops-wiki/validation/quickstart-run.md per FR-007 (missing)
- [X] T032 Collect pilot feedback metric and update acceptance status in specs/002-read-devops-wiki/validation/final-report.md per SC-004 (partial)

## Phase 8: Convergence

- [X] T033 Add wiki source-attribution instruction to `.github/copilot-instructions.md` so Stan cites Data Science Pool Azure DevOps wiki (not `docs/strategy-playbook.md`) for wiki-backed prompts per T028/US2/AC1/FR-002 (missing)
- [X] T034 Add wiki-response template to `docs/stan-agent/response-templates.md` with source attribution rules and example for wiki content retrieval per T028/US2/AC1/FR-002 (missing)

## Phase 9: Convergence

- [ ] T035 Run end-to-end source-transparency scenario S3 after T033/T034 and record updated evidence in specs/002-read-devops-wiki/validation/us2-results.md per US2/AC1 (partial)
- [ ] T036 Reconcile scenario S3 status and acceptance outcome in specs/002-read-devops-wiki/validation/quickstart-run.md and specs/002-read-devops-wiki/validation/final-report.md per FR-002/FR-003/SC-001 (partial)
