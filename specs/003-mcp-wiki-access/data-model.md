# Data Model: Azure DevOps MCP Wiki Access

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

- Description: A readable page from the Data Science Pool Azure DevOps wiki, retrieved through the MCP Server.
- Fields:
  - `pageTitle` (string): Human-readable wiki page title.
  - `pagePath` (string): Unique path within wiki hierarchy.
  - `content` (string): Retrieved page body (from `wiki get_page_content` tool).
  - `lastUpdated` (string|null): Optional page recency metadata.
  - `wikiId` (string): Identifier of the parent wiki (from `wiki list_wikis` or `wiki get_wiki` tool).
- Validation rules:
  - `pageTitle` and `pagePath` MUST be present for successful retrieval.
  - `content` MAY be empty only when retrieval result indicates not found or no readable content.

## Entity: WikiAccessResult

- Description: Outcome of a wiki retrieval attempt for a query, resolved through MCP tool calls.
- Fields:
  - `status` (enum): `success`, `not_found`, `unavailable`, `access_denied`, `no_content`.
  - `matchedPage` (WikiPage|null): Retrieved page on success.
  - `message` (string): User-facing explanation aligned with status.
  - `mcpToolUsed` (string): The MCP tool used for retrieval (e.g., `wiki get_page_content`, `mcp_ado_search_wiki`).
- Validation rules:
  - `status` MUST be one of the defined enum values.
  - `matchedPage` MUST be present when `status=success`.
  - `matchedPage` MUST be absent when status is not success.

### Canonical Status Definitions

- `success`: Requested wiki topic/page resolved and readable through MCP tool call.
- `not_found`: No matching wiki topic/page exists (MCP tool returned empty/no result for the given page path or search query).
- `no_content`: Matching page exists but has no readable content (MCP tool returned page metadata but empty content body).
- `unavailable`: MCP Server connection is temporarily unavailable (connection error, timeout, or transport failure).
- `access_denied`: MCP Server is reachable but requested page/topic is not readable for the current identity (MCP returned authorization error).

## Entity: ResponseContext

- Description: Conversation-scoped context for follow-up wiki questions.
- Fields:
  - `lastResolvedTopic` (string|null): Most recent successfully answered topic.
  - `lastResolvedPagePath` (string|null): Most recent page path used for response.
  - `lastWikiId` (string|null): Most recent wiki identifier for scoped follow-up.
  - `sourceScope` (string): Must remain `Data Science Pool Azure DevOps wiki`.
  - `accessChannel` (string): Must remain `Azure DevOps MCP Server`.
- Validation rules:
  - `sourceScope` MUST remain fixed to the approved wiki scope.
  - `accessChannel` MUST identify the MCP Server as the transport method.
  - Follow-up resolution MUST prefer `lastResolvedPagePath` when user query is referential.

### Follow-up Resolution Rules

- If user refers to "that page" or "the previous topic", system resolves against `lastResolvedPagePath` first.
- If `lastResolvedPagePath` is null but `lastResolvedTopic` exists, system resolves by topic.
- If both are null or ambiguous, system asks a clarifying question before retrieval.

## Entity: MCPConnectionConfig

- Description: Describes how Stan reaches the Azure DevOps wiki through the MCP Server.
- Fields:
  - `configFile` (string): Path to the MCP configuration file (`.vscode/mcp.json`).
  - `serverName` (string): Named server entry in the MCP config (e.g., `ado-remote-mcp` or `ado`).
  - `domains` (string[]): Loaded tool domains, MUST include `core` and `wiki`.
  - `deploymentMode` (enum): `remote` (recommended) or `local`.
  - `authMethod` (string): Authentication approach — `vs-code-oauth` (remote) or `pat` (local).
  - `configuredTools` (string[]): Available wiki-read tool list derived from the MCP toolset.
- Validation rules:
  - `domains` MUST include at least `core` and `wiki`.
  - `configuredTools` MUST include at least one page-content retrieval tool (e.g., `wiki get_page_content` or equivalent).

## Entity: WikiSourceResult (retained from 002)

- Description: The returned wiki lookup outcome for user-facing messaging.
- This entity is unchanged from the 002 data model. It captures the status and user-facing message for display.

## Relationships

- `UserQuery` triggers one or more `MCPConnectionConfig`-mediated MCP tool calls.
- MCP tool calls produce a `WikiAccessResult` which may contain one `WikiPage` when successful.
- `ResponseContext` is updated from successful `WikiAccessResult` and informs subsequent `UserQuery` handling.
- `WikiAccessResult` maps MCP-level errors to the canonical `status` enum for the existing `WikiSourceResult` entity.
