# Phase 0 Research: Azure DevOps MCP Wiki Access

## Decision 1: MCP Server deployment mode

- Decision: Use the Remote (HTTP) MCP Server for production, with the Local (stdio) MCP Server documented as an alternative.
- Rationale: The Azure DevOps Remote MCP Server is now in public preview and is the recommended path. It eliminates the Node.js/npx dependency, provides streamable HTTP transport, and is managed by Azure DevOps directly. The local server is documented as a fallback for scenarios where remote is unavailable or when a specific stdio setup is required.
- Alternatives considered:
  - Local (stdio) MCP Server only: rejected because remote is the recommended forward-looking path per Microsoft's documentation.
  - REST API continued: rejected per FR-002 — this feature explicitly replaces REST with MCP.

## Decision 2: MCP Server configuration format

- Decision: Use `.vscode/mcp.json` in the repository root with domain-filtered tool loading (`-d core,wiki`).
- Rationale: This is the standard VS Code MCP extension configuration file. Domain filtering limits the loaded toolset to only what Stan needs (core + wiki), reducing context overhead and improving tool selection accuracy.
- Alternatives considered:
  - Load all domains (default): rejected because unnecessary tools (pipelines, work-items, etc.) increase context noise and risk scope creep.
  - Global `mcp.json` in user config directory: rejected because the repo-scoped file is shareable with the team and version-controlled.

## Decision 3: Wiki tools available through MCP

- Decision: Document the following MCP wiki tools as the access surface for Stan:

| MCP Tool | Action | Purpose |
|---|---|---|
| `wiki` | `list_wikis` | List all wikis in an org/project |
| `wiki` | `get_wiki` | Get wiki details (by ID or name) |
| `wiki` | `list_pages` | List pages in a wiki hierarchy |
| `wiki` | `get_page` | Get wiki page metadata (path, title, without content body) |
| `wiki` | `get_page_content` | Retrieve full wiki page content body |
| `mcp_ado_search_wiki` | — | Search wiki pages by keyword |

- Rationale: These six tools provide complete wiki-read capability — discovery (list wikis, list pages), targeted retrieval (get page, get page content), and search (search wiki). The `wiki_upsert_page` tool (write) is excluded per the read-only scope.
- Alternatives considered:
  - Only use `get_page_content`: rejected because Stan needs discovery tools to resolve topic-to-page mappings before content retrieval.
  - Only use search-based retrieval: rejected because it depends on keyword match quality; direct page path retrieval is more reliable for known pages.

## Decision 4: Authentication model for MCP

- Decision: The Remote MCP Server uses the user's Azure DevOps identity (browser-based OAuth) when accessed through VS Code. For the local server, the existing DevOps PAT can be used via `--authentication pat` flag with the `AZURE_DEVOPS_PAT` environment variable.
- Rationale: The Remote MCP Server handles auth transparently through VS Code's sign-in context — no PAT management needed in the common case. The local server PAT path reuses the existing `AZURE_DEVOPS_PAT` environment variable from the current REST-based setup, satisfying the "no new credential infrastructure" assumption from the spec.
- Alternatives considered:
  - Azure CLI authentication (`--authentication azcli`): technically viable but adds a dependency on Azure CLI being installed and authenticated.
  - OAuth device flow: more complex setup, unnecessary when VS Code provides seamless auth for remote mode.

## Decision 5: Error mapping from MCP to contract outcomes

- Decision: Map MCP failure modes to the existing wiki-read contract outcome matrix:

| MCP Behavior | Contract Outcome |
|---|---|
| Tool returns page content successfully | `success` |
| Tool returns empty/no result for page/topic | `not_found` |
| Tool returns page metadata but empty content | `no_content` |
| MCP Server connection error / timeout | `unavailable` |
| MCP Server returns 403/unauthorized | `access_denied` |

- Rationale: The MCP Server abstracts REST API details, so error handling shifts from REST HTTP status codes to MCP tool return values and connection states. This mapping preserves backward compatibility with the existing contract outcome matrix.
- Alternatives considered:
  - Expose raw MCP error codes to users: rejected — the abstraction layer should simplify, not complicate, error handling.

## Decision 6: File cleanup scope

- Decision: Remove REST-specific content from `docs/stan-agent/devops-access.md` and replace with MCP Server configuration docs. Retain the file as a reference for MCP-based access.
- Rationale: The file purpose (documenting how Stan accesses the DevOps wiki) remains valid; only the transport mechanism changes. Removing the file entirely would break existing references in the repo.
- Alternatives considered:
  - Keep devops-access.md unchanged: rejected because it documents the REST approach being removed (FR-011).
  - Create a new mcp-access.md and delete devops-access.md: rejected per minimal-changes principle — updating in place is simpler.

## Decision 7: copilot-instructions.md update

- Decision: Update `.github/copilot-instructions.md` to point the wiki-read contract reference from `specs/002-read-devops-wiki/contracts/wiki-read-contract.md` to `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md`.
- Rationale: This ensures Stan's agent instructions reference the updated MCP-based contract. The 002 contract is retained as a historical artifact but is no longer the active reference.
- Alternatives considered:
  - Keep referencing 002: rejected because the 003 feature supersedes 002 for the wiki-read capability.
