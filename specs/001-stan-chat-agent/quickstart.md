# Quickstart Validation Guide: Stan Chat Agent for Quarterly Strategy

## Prerequisites

- Feature spec and plan exist in `specs/001-stan-chat-agent/`.
- Source-of-truth playbook is available at `docs/strategy-playbook.md`.
- Chat behavior contract is available at `specs/001-stan-chat-agent/contracts/chat-behavior-contract.md`.

## Validation Scenario 1: Quarterly structure answer

1. Ask Stan: "Give me the quarterly strategy session structure."
2. Verify response includes:
   - Session purpose.
   - Total duration (`3-4 hours`).
   - All 7 sections in correct order.
   - English response language.
3. Expected outcome:
   - Response is in-scope and complete per `FR-001` to `FR-004`.

## Validation Scenario 2: Deliverable format answer

1. Ask Stan: "What output should we capture after the session?"
2. Verify response includes all six summary elements from the strategy summary template.
3. Expected outcome:
   - Deliverable format is complete per `FR-005`.

## Validation Scenario 3: Out-of-scope prompt

1. Ask Stan a non-quarterly topic question.
2. Verify response includes:
   - Short scope-limit statement.
   - Redirect to supported quarterly-structure topics.
3. Expected outcome:
   - Out-of-scope behavior conforms to `FR-007`.

## Validation Scenario 4: Annual mission edge case

1. Ask Stan: "What is our annual mission and positioning?"
2. Verify response includes:
   - At most one sentence of annual context.
   - Redirect to quarterly strategy structure.
   - English response language.
3. Expected outcome:
   - Behavior conforms to `FR-009`.

## Validation Scenario 5: Mixed-query behavior

1. Ask Stan one prompt with both in-scope and out-of-scope parts.
2. Verify response:
   - Answers in-scope quarterly part fully first.
   - Adds short scope-limit statement for out-of-scope part.
3. Expected outcome:
   - Behavior conforms to `FR-010`.

## Validation Scenario 6: Timing adaptation behavior

1. Ask Stan for alternative durations per section.
2. Verify response:
   - Provides adapted timing proposal.
   - States that playbook timings are indicative guidance.
3. Expected outcome:
   - Behavior conforms to `FR-011`.

## Validation Scenario 7: Dutch input, English output

1. Ask Stan: "Geef me de agenda van de kwartaalstrategiesessie."
2. Verify response:
   - Is fully in English.
   - Keeps quarterly structure content accurate and in scope.
3. Expected outcome:
   - Behavior conforms to `FR-012` and `SC-005`.

## Exit Criteria

- All seven scenarios pass in manual chat validation.
- No response violates scope boundary rules in contract.
- All tested responses are in English for v1.

## Evidence Artifacts

- US1 prompts: `specs/001-stan-chat-agent/validation/us1-structure.md`
- US1 results: `specs/001-stan-chat-agent/validation/us1-results.md`
- US2 results: `specs/001-stan-chat-agent/validation/us2-results.md`
- US3 results: `specs/001-stan-chat-agent/validation/us3-results.md`
- Consolidated quickstart run: `specs/001-stan-chat-agent/validation/quickstart-run.md`
- Link check: `specs/001-stan-chat-agent/validation/link-check.md`
- Final acceptance mapping: `specs/001-stan-chat-agent/validation/final-report.md`
