# Phase 0 Research: Read Azure DevOps Wiki

## Decision 1: Source boundary for external knowledge

- Decision: Limit external retrieval to the Data Science Pool Azure DevOps wiki only.
- Rationale: This satisfies feature scope and prevents uncontrolled source expansion in v1.
- Alternatives considered:
  - Include other Azure DevOps artifacts (boards/repos/pipelines): rejected because out of current feature scope.
  - Multi-system retrieval in v1: rejected to keep behavior predictable.

## Decision 2: Read-only access model

- Decision: Treat wiki interaction as strictly read-only.
- Rationale: User requirement is retrieval only, and read-only minimizes risk and operational complexity.
- Alternatives considered:
  - Allow wiki edits from chat: rejected because not requested and higher governance risk.

## Decision 3: Error taxonomy for user feedback

- Decision: Use explicit user-facing outcomes for not found, unavailable, and access denied cases.
- Rationale: Distinct failure messages are easier to act on and align with FR-005 and FR-006.
- Alternatives considered:
  - Generic retrieval failure only: rejected because it obscures remediation.

## Decision 4: Scope-preserving response behavior

- Decision: Preserve existing quarterly strategy support while adding wiki-backed answers, and clearly indicate wiki-source usage when asked.
- Rationale: This protects existing behavior commitments and adds transparency about sourced information.
- Alternatives considered:
  - Replace existing strategy behavior with wiki-only behavior: rejected due to regression risk against FR-008.

## Decision 5: Follow-up continuity

- Decision: Support follow-up questions by retaining conversational context about the last retrieved wiki topic/page.
- Rationale: This is required by FR-007 and improves usability without broadening data scope.
- Alternatives considered:
  - Require users to repeat full page/topic in every turn: rejected due to poor user experience.

## Decision 6: Validation approach

- Decision: Use contract vectors plus quickstart prompt scenarios for manual end-to-end verification.
- Rationale: Repository is documentation-first; scenario validation provides clear acceptance evidence before implementation.
- Alternatives considered:
  - Add runtime test tooling in planning phase: rejected per minimal-tooling and documentation-first constraints.

## Shared Retrieval Outcome Matrix

| Outcome | Meaning | User-facing response requirement |
|---|---|---|
| success | Matching wiki content retrieved | Provide relevant wiki-derived answer |
| not_found | No matching page/topic found | State not found and suggest refinement |
| no_content | Page exists but has no readable body | State no readable content and suggest adjacent topic |
| unavailable | Wiki service/access path temporarily unavailable | State temporary unavailability and suggest retry |
| access_denied | Request targets content not readable by current identity | State restricted access and suggest requesting permission |
