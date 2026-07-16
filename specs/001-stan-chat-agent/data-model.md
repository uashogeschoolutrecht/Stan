# Data Model: Stan Chat Agent for Quarterly Strategy

## Entity: QuarterlyStrategySession

- Description: Canonical representation of one quarterly strategy session flow.
- Fields:
  - `purpose` (string): Session purpose statement.
  - `duration` (string): Total target duration (`3-4 hours`).
  - `sections` (list<SessionSection>): Ordered agenda sections.
  - `summaryTemplate` (StrategySummaryTemplate): Expected post-session deliverable shape.
- Validation rules:
  - `sections` MUST contain exactly 7 ordered items matching playbook sequence.
  - `duration` MUST remain aligned with playbook total duration guidance.

## Entity: SessionSection

- Description: A single agenda section in the quarterly strategy meeting.
- Fields:
  - `order` (integer): Position in session (1..7).
  - `title` (string): Section title.
  - `suggestedDurationMinutes` (integer): Indicative section timing.
  - `focus` (string): Main discussion objective.
  - `expectedOutput` (string|null): Tangible output if defined.
- Validation rules:
  - `order` MUST be unique across the 7 sections.
  - `title` MUST match the playbook section headings.
  - `suggestedDurationMinutes` MAY be adapted in responses, but base guidance must be acknowledged.

## Entity: StrategySummaryTemplate

- Description: Structure of the one-page strategy summary output.
- Fields:
  - `keyDevelopments` (string)
  - `strategicPriorities` (string)
  - `startStopDecisions` (string)
  - `businessOpportunities` (string)
  - `teamLearningGoals` (string)
  - `actionsAndOwners` (string)
- Validation rules:
  - All six elements MUST be present when asked for deliverable format.

## Entity: ScopeBoundary

- Description: Rules for what Stan can and cannot answer in v1.
- Fields:
  - `inScopeTopics` (list<string>): Quarterly session structure topics.
  - `outOfScopeTopics` (list<string>): Topics beyond v1 domain.
  - `responseLanguage` (string): Required default response language (`English`).
  - `redirectPattern` (string): Required out-of-scope redirect style.
  - `mixedQueryPolicy` (string): In-scope-first, then scope-limit behavior.
  - `annualContextPolicy` (string): One-sentence annual context maximum.
- Validation rules:
  - Responses MUST be in English for v1.
  - Out-of-scope responses MUST include a scope-limit statement.
  - Mixed queries MUST return in-scope content before scope-limit note.
  - Annual mission prompts MUST not exceed one sentence before redirect.

## Relationships

- `QuarterlyStrategySession` 1..1 contains `StrategySummaryTemplate`.
- `QuarterlyStrategySession` 1..7 contains `SessionSection`.
- `ScopeBoundary` governs response behavior for all entities.
