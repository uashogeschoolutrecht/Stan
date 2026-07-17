# Data Model: Read Azure DevOps Wiki

## Entity: UserQuery

- Description: A user message asking for information that may map to wiki content.
- Fields:
  - `queryText` (string): User-provided natural language request.
  - `requestedTopic` (string|null): Parsed topic intent when available.
  - `requestedPageHint` (string|null): Optional explicit page hint/path.
  - `conversationId` (string): Conversation context identifier.
- Validation rules:
  - `queryText` MUST be non-empty.
  - At least one of `requestedTopic` or `requestedPageHint` SHOULD be derivable for wiki retrieval.

## Entity: WikiPage

- Description: A readable page from the Data Science Pool Azure DevOps wiki.
- Fields:
  - `pageTitle` (string): Human-readable wiki page title.
  - `pagePath` (string): Unique path within wiki hierarchy.
  - `content` (string): Retrieved page body.
  - `lastUpdated` (string|null): Optional page recency metadata.
- Validation rules:
  - `pageTitle` and `pagePath` MUST be present for successful retrieval.
  - `content` MAY be empty only when retrieval result indicates not found or no readable content.

## Entity: WikiAccessResult

- Description: Outcome of a wiki retrieval attempt for a query.
- Fields:
  - `status` (enum): `success`, `not_found`, `unavailable`, `access_denied`, `no_content`.
  - `matchedPage` (WikiPage|null): Retrieved page on success.
  - `message` (string): User-facing explanation aligned with status.
- Validation rules:
  - `status` MUST be one of the defined enum values.
  - `matchedPage` MUST be present when `status=success`.
  - `matchedPage` MUST be absent when status is not success.

### Canonical Status Definitions

- `success`: Requested wiki topic/page resolved and readable.
- `not_found`: No matching wiki topic/page exists.
- `no_content`: Matching page exists but has no readable content.
- `unavailable`: Wiki source cannot be reached temporarily.
- `access_denied`: Wiki source is reachable, but requested page/topic is not readable for current identity.

## Entity: ResponseContext

- Description: Conversation-scoped context for follow-up wiki questions.
- Fields:
  - `lastResolvedTopic` (string|null): Most recent successfully answered topic.
  - `lastResolvedPagePath` (string|null): Most recent page path used for response.
  - `sourceScope` (string): Must remain `Data Science Pool Azure DevOps wiki`.
- Validation rules:
  - `sourceScope` MUST remain fixed to the approved wiki scope.
  - Follow-up resolution MUST prefer `lastResolvedTopic` or `lastResolvedPagePath` when user query is referential.

### Follow-up Resolution Rules

- If user refers to "that page" or "the previous topic", system resolves against `lastResolvedPagePath` first.
- If `lastResolvedPagePath` is null but `lastResolvedTopic` exists, system resolves by topic.
- If both are null or ambiguous, system asks a clarifying question before retrieval.

## Relationships

- `UserQuery` triggers one `WikiAccessResult`.
- `WikiAccessResult` may contain one `WikiPage` when successful.
- `ResponseContext` is updated from successful `WikiAccessResult` and informs subsequent `UserQuery` handling.
