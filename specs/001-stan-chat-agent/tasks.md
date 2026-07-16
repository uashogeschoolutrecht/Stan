# Tasks: Stan Chat Agent for Quarterly Strategy

**Input**: Design documents from /specs/001-stan-chat-agent/

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: No automated test framework requested; tasks use manual chat validation evidence files.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create documentation scaffolding for Stan agent implementation.

- [X] T001 Create Stan agent docs folder and landing page in docs/stan-agent/index.md
- [X] T002 Create validation evidence folder and template in specs/001-stan-chat-agent/validation/README.md
- [X] T003 [P] Create implementation notes log in specs/001-stan-chat-agent/implementation-notes.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared knowledge and baseline agent configuration required by all stories.

**CRITICAL**: User story work starts only after this phase is complete.

- [X] T004 Create canonical quarterly structure reference from playbook in docs/stan-agent/quarterly-structure.md
- [X] T005 [P] Create scope boundary policy reference in docs/stan-agent/scope-boundaries.md
- [X] T006 [P] Create reusable response templates in docs/stan-agent/response-templates.md
- [X] T007 Update global Copilot guidance to include Stan sources in .github/copilot-instructions.md
- [X] T008 Create Stan agent definition file in .github/agents/stan.agent.md

**Checkpoint**: Foundation complete; user stories can be implemented independently.

---

## Phase 3: User Story 1 - Ask for quarterly session structure (Priority: P1) 🎯 MVP

**Goal**: Stan answers quarterly structure questions with correct purpose, duration, section order, and English-first behavior.

**Independent Test**: Ask Stan for structure, timing, and Dutch-input prompts; verify English output and seven ordered sections with guidance-compliant timing adaptations.

### Implementation for User Story 1

- [X] T009 [US1] Implement structure response rules in .github/agents/stan.agent.md
- [X] T010 [P] [US1] Add section order-duration-output matrix in docs/stan-agent/quarterly-structure.md
- [X] T011 [P] [US1] Add timing adaptation answer patterns in docs/stan-agent/response-templates.md
- [X] T012 [US1] Add US1 prompt set and expected outcomes in specs/001-stan-chat-agent/validation/us1-structure.md
- [X] T013 [US1] Record US1 manual validation evidence in specs/001-stan-chat-agent/validation/us1-results.md

**Checkpoint**: User Story 1 is independently functional and demonstrable.

---

## Phase 4: User Story 2 - Ask for deliverable format (Priority: P2)

**Goal**: Stan provides the one-page strategy summary format with all six required elements.

**Independent Test**: Ask Stan what to capture after a session; verify all summary elements are present in English.

### Implementation for User Story 2

- [X] T014 [P] [US2] Create one-page deliverable reference in docs/stan-agent/deliverable-format.md
- [X] T015 [US2] Implement deliverable-format response path in .github/agents/stan.agent.md
- [X] T016 [P] [US2] Add deliverable-format response examples in docs/stan-agent/response-templates.md
- [X] T017 [US2] Add and execute US2 validation script prompts in specs/001-stan-chat-agent/validation/us2-results.md

**Checkpoint**: User Story 2 works independently from other stories.

---

## Phase 5: User Story 3 - Keep answers in scope (Priority: P3)

**Goal**: Stan handles out-of-scope, mixed, and annual-mission prompts with required boundary behavior.

**Independent Test**: Run out-of-scope, mixed-query, and annual-context prompts; verify redirect pattern, one-sentence annual limit, and in-scope-first ordering.

### Implementation for User Story 3

- [X] T018 [P] [US3] Add out-of-scope and mixed-query decision table in docs/stan-agent/scope-boundaries.md
- [X] T019 [US3] Implement scope enforcement rules in .github/agents/stan.agent.md
- [X] T020 [P] [US3] Add language-policy and Dutch-input boundary examples in docs/stan-agent/response-templates.md
- [X] T021 [US3] Add and execute US3 validation prompt runs in specs/001-stan-chat-agent/validation/us3-results.md

**Checkpoint**: User Story 3 is independently functional and compliant with scope constraints.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Consolidate validation, docs consistency, and release-ready guidance.

- [X] T022 [P] Create consolidated quickstart run evidence in specs/001-stan-chat-agent/validation/quickstart-run.md
- [X] T023 Update usage and navigation for Stan agent in README.md
- [X] T024 Update feature quickstart references to new validation artifacts in specs/001-stan-chat-agent/quickstart.md
- [X] T025 [P] Run markdown link consistency pass and capture outcomes in specs/001-stan-chat-agent/validation/link-check.md
- [X] T026 Create final acceptance summary mapped to FR-001..FR-012 in specs/001-stan-chat-agent/validation/final-report.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): No dependencies.
- Foundational (Phase 2): Depends on Setup completion; blocks all user stories.
- User Stories (Phases 3-5): Depend on Foundational completion.
- Polish (Phase 6): Depends on completion of selected user stories.

### User Story Dependencies

- US1 (P1): Starts after Phase 2; no dependency on US2/US3.
- US2 (P2): Starts after Phase 2; independent from US1/US3 except shared files.
- US3 (P3): Starts after Phase 2; independent from US1/US2 except shared files.

### Dependency Graph

- Phase 1 -> Phase 2 -> {Phase 3, Phase 4, Phase 5} -> Phase 6
- Recommended delivery order: US1 (MVP) -> US2 -> US3

---

## Parallel Opportunities

- Setup: T003 can run in parallel with T001-T002.
- Foundational: T005 and T006 can run in parallel after T004 starts.
- US1: T010 and T011 can run in parallel after T009 starts.
- US2: T014 and T016 can run in parallel; T017 after T015.
- US3: T018 and T020 can run in parallel; T021 after T019.
- Polish: T022 and T025 can run in parallel.

### Parallel Example: User Story 1

- Task: T010 [US1] docs/stan-agent/quarterly-structure.md
- Task: T011 [US1] docs/stan-agent/response-templates.md

### Parallel Example: User Story 2

- Task: T014 [US2] docs/stan-agent/deliverable-format.md
- Task: T016 [US2] docs/stan-agent/response-templates.md

### Parallel Example: User Story 3

- Task: T018 [US3] docs/stan-agent/scope-boundaries.md
- Task: T020 [US3] docs/stan-agent/response-templates.md

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate with specs/001-stan-chat-agent/validation/us1-results.md.
4. Demo Stan structure-answer capability.

### Incremental Delivery

1. Ship US1 for immediate value.
2. Add US2 deliverable-format support.
3. Add US3 scope enforcement behavior.
4. Finish Phase 6 validation consolidation.

### Parallel Team Strategy

1. Team member A: .github/agents/stan.agent.md tasks.
2. Team member B: docs/stan-agent/*.md reference and template tasks.
3. Team member C: specs/001-stan-chat-agent/validation/*.md evidence tasks.

---

## Notes

- [P] marks tasks that are parallelizable.
- [US1]/[US2]/[US3] labels map implementation to specific user stories.
- All tasks include explicit file paths.
- No automated tests were added because specification did not request a test framework.
