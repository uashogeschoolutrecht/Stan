# Phase 0 Research: Stan Chat Agent for Quarterly Strategy

## Decision 1: Scope boundaries

- Decision: Hard-bound Stan knowledge to one authoritative source (`docs/strategy-playbook.md`) and to quarterly strategy meeting structure topics only.
- Rationale: This maximizes consistency, keeps behavior testable, and aligns with the constitution source-of-truth rule.
- Alternatives considered:
  - Soft boundary with broader strategy advice: rejected due to drift risk and harder validation.
  - Multi-source knowledge in v1: rejected to keep documentation scope lightweight.

## Decision 2: Out-of-scope handling

- Decision: Use a fixed response pattern for out-of-scope prompts: short scope-limit statement plus redirect to supported quarterly-structure topics.
- Rationale: Predictable and helpful behavior avoids dead-end refusals while preserving boundaries.
- Alternatives considered:
  - Refuse without redirect: rejected for poor user experience.
  - Best-effort answer outside scope: rejected because it conflicts with v1 boundary requirements.

## Decision 3: Annual mission-positioning edge case

- Decision: For annual mission-positioning prompts, provide at most one sentence of context, then redirect to quarterly strategy structure.
- Rationale: Preserves user orientation while keeping answers primarily in v1 scope.
- Alternatives considered:
  - Full annual explanation: rejected because annual focus is out of v1 scope.
  - Immediate refusal: rejected as too rigid.

## Decision 4: Mixed-query behavior

- Decision: For prompts containing both in-scope and out-of-scope parts, answer the in-scope quarterly part fully first, then add a short scope-limit note for the out-of-scope part.
- Rationale: Users still receive useful output in one turn while scope remains explicit.
- Alternatives considered:
  - Reject entire mixed prompt: rejected due to unnecessary friction.
  - Ignore out-of-scope part silently: rejected due to unclear boundaries.

## Decision 5: Timing-variation handling

- Decision: Treat section timings as indicative guidance; allow adapted section timing proposals when requested and explicitly note the guidance nature.
- Rationale: Supports practical meeting constraints while staying faithful to the playbook structure and intent.
- Alternatives considered:
  - Enforce fixed durations: rejected as too rigid for real sessions.
  - Freely alter timings without note: rejected due to loss of source alignment.

## Decision 6: Conversational interface contract pattern

- Decision: Define a markdown contract with normative language (MUST/SHOULD/MAY), explicit response ordering, and acceptance vectors.
- Rationale: Keeps implementation lightweight, reviewable, and testable in a documentation-first repository.
- Alternatives considered:
  - Free-form guidelines only: rejected due to ambiguity.
  - JSON schema-only contract: rejected because markdown is more maintainable for this repo audience.
