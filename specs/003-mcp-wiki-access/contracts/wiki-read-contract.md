# Chat Behavior Contract: Stan Azure DevOps Wiki Read (v2 — MCP Transport)

## Purpose

Define user-visible behavior guarantees for Stan when answering with Data Science Pool Azure DevOps wiki content, accessed through the Azure DevOps MCP Server (VS Code MCP Extension).

## Version History

- **v1** (002-read-devops-wiki): REST API-based wiki read. Superseded by v2.
- **v2** (003-mcp-wiki-access): MCP Server-based wiki read. Replaces v1 transport.

## Scope

- In scope:
  - Read-only retrieval from Data Science Pool Azure DevOps wiki via the Azure DevOps MCP Server.
  - Topic/page-based wiki question answering.
  - Follow-up questions about previously retrieved wiki information.
  - Explicit handling of not-found, unavailable, and access-denied outcomes.
- Out of scope:
  - Writing or editing wiki pages (`wiki_upsert_page` MCP tool is excluded).
  - Accessing Azure DevOps artifacts other than the wiki (Boards, Repos, Pipelines, etc.).
  - Replacing existing quarterly strategy behavior.

## Transport Mechanism

- Wiki content is retrieved through the **Azure DevOps MCP Server**, configured in `.vscode/mcp.json` with the `wiki` domain loaded.
- The Remote MCP Server (`type: "http"` at `https://mcp.dev.azure.com/{organization}`) is the recommended deployment mode.
- The Local MCP Server (`type: "stdio"` with `npx -y @azure-devops/mcp`) is supported as an alternative.
- The REST API-based wiki read path from v1 is removed entirely — no fallback or dual-path is retained (FR-011).

## Source Anchoring Rules

- Stan MUST restrict external retrieval in this feature to the Data Science Pool Azure DevOps wiki.
- Stan MUST NOT retrieve data from Boards, Repos, Pipelines, Test Plans, or any non-wiki Azure DevOps area.
- Stan MUST preserve existing quarterly strategy guidance behavior from repository docs.
- Stan MUST indicate wiki source usage when users ask where information came from.

## Retrieval Outcome Matrix

| Status | Required User Message | Required Next Guidance |
|---|---|---|
| success | Relevant answer from wiki content | Optional follow-up prompt |
| not_found | Requested page/topic not found | Suggest topic/page refinement |
| no_content | Page exists but no readable content | Suggest adjacent page/topic |
| unavailable | Wiki is temporarily unavailable through MCP Server | Suggest retry later |
| access_denied | Access is restricted | Suggest requesting access |

## Response Behavior Rules

### Successful wiki retrieval

- Stan MUST provide a relevant answer derived from retrieved wiki content.
- Stan SHOULD align wording with the user request while preserving wiki meaning.

### Topic-based retrieval

- Stan MUST resolve topic-style prompts to the most relevant wiki page(s) using MCP tools (e.g., `mcp_ado_search_wiki` for keyword search, or `wiki get_page`/`wiki get_page_content` for known paths).
- Stan MUST summarize retrieved topic content before optional detail expansion.

### Page-specific retrieval

- Stan MUST honor explicit page hints/path when supplied by the user, using `wiki get_page` + `wiki get_page_content` tools.
- Stan MUST keep response content consistent with the referenced page.

### Out-of-scope content request

- Stan MUST state that requested content is outside current wiki scope when not covered by available wiki content.
- Stan SHOULD suggest rephrasing with a specific wiki topic or page.

### Source attribution

- When asked for source, Stan MUST explicitly mention the Data Science Pool Azure DevOps wiki.
- Stan SHOULD include the resolved page title/path when available.

### Non-wiki scope guardrail

- For requests targeting Boards, Repos, Pipelines, or other non-wiki Azure DevOps areas, Stan MUST return a wiki-only scope-limit response.
- Stan SHOULD redirect user to ask a wiki-topic or wiki-page-specific question.

### Not found

- Stan MUST state that the requested wiki page/topic could not be found.
- Stan SHOULD suggest a nearby page name or topic refinement when available.

### No readable content

- Stan MUST state that the page exists but has no readable content.
- Stan SHOULD suggest an adjacent page/topic to continue.

### Temporary unavailability

- Stan MUST state that wiki content is currently unavailable through the Azure DevOps MCP Server.
- Stan SHOULD suggest retrying later.
- Stan SHOULD avoid presenting stale content as current when unavailable.

### Access restricted

- Stan MUST state that wiki access is restricted for the requested page/topic.
- Stan SHOULD suggest requesting access from the wiki owner/admin.
- Stan MUST avoid implying missing page when the condition is permission-related.

### Follow-up queries

- Stan MUST support follow-up questions using conversation context from the most recently retrieved wiki topic/page.
- Stan MUST ask for clarification when follow-up intent cannot be resolved from context.

## MCP Tool Mapping

| Retrieval Need | MCP Tool(s) | Notes |
|---|---|---|
| Find wikis in the org | `wiki list_wikis` | Returns wiki ID and name |
| Get wiki details | `wiki get_wiki` | Requires wiki ID |
| List pages in a wiki | `wiki list_pages` | Returns page hierarchy |
| Get page metadata | `wiki get_page` | Returns path, title, without content |
| Get full page content | `wiki get_page_content` | Primary content retrieval tool |
| Search wiki by keyword | `mcp_ado_search_wiki` | Full-text search with optional filters |

## MCP Error Mapping

| MCP Behavior | Contract Outcome |
|---|---|
| Tool returns page content successfully | `success` |
| Tool returns empty/no result for page/topic | `not_found` |
| Tool returns page metadata but empty content | `no_content` |
| MCP Server connection error / timeout | `unavailable` |
| MCP Server returns authorization error | `access_denied` |

## Configuration Reference

For detailed MCP server setup instructions, see `docs/stan-agent/devops-access.md`.

### Remote MCP Server (recommended)

```json
{
  "servers": {
    "ado-remote-mcp": {
      "url": "https://mcp.dev.azure.com/HogeschoolUtrecht",
      "type": "http"
    }
  }
}
```

### Local MCP Server (alternative)

```json
{
  "servers": {
    "ado": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "HogeschoolUtrecht", "-d", "core", "wiki"]
    }
  }
}
```

## Acceptance Test Vectors

1. Prompt: "What does our DevOps wiki say about quarterly prep?"
   - Expected: Relevant summary derived from wiki content via MCP Server.
2. Prompt: "Which source did you use?"
   - Expected: States Data Science Pool Azure DevOps wiki as source.
3. Prompt: "Open wiki page X that I do not have access to."
   - Expected: Clear access-restricted message and request-access suggestion.
4. Prompt: "Get wiki page Y" when MCP Server is unavailable.
   - Expected: Clear unavailable message and retry guidance.
5. Prompt: "Use the previous page and explain the decision points."
   - Expected: Follow-up answer uses prior retrieved page context.
6. Prompt: "Also read boards and pipelines for this."
   - Expected: Scope-limit note that this feature is wiki-only.
7. Prompt: "Summarize our wiki topic on quarterly preparation."
   - Expected: Topic-based wiki summary from relevant page content via MCP.
8. Prompt: "Use page /Strategy/Quarterly-Prep and list key decisions."
   - Expected: Response aligned to that page content and decision points.

## Versioning

- Contract version: `v2`
- Previous version: `v1` (REST API-based, at `specs/002-read-devops-wiki/contracts/wiki-read-contract.md`)
- Compatibility note: v2 replaces v1 transport. Behavior guarantees are preserved from v1. Expanding beyond wiki read-only scope MUST bump contract version and add vectors.
