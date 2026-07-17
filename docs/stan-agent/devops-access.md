# DevOps Wiki Access (MCP Server)

## Purpose

Describe how Stan reads Azure DevOps wiki content at runtime through the Azure DevOps MCP Server.

## Scope

- Read-only access to Azure DevOps wiki content via MCP Server tools.
- No write/update operations (`wiki_upsert_page` MCP tool is excluded).
- No Boards/Repos/Pipelines access as part of this capability.

## Transport Mechanism

Wiki content is retrieved through the **Azure DevOps MCP Server**, configured in `.vscode/mcp.json` with the `wiki` domain loaded. The MCP Server replaces the previous REST API-based wiki read path — no fallback or dual-path is retained.

## VS Code Setup

1. Install the Azure DevOps MCP Server / MCP extension support in VS Code if it is not already available in your environment.
2. Create `.vscode/mcp.json` at the repository root.
3. Add one of the server configurations below.
4. Save the file and open the VS Code MCP view.
5. Enable or start the configured Azure DevOps MCP connection.
6. Confirm the connection shows as connected and that the `wiki` domain/tools are available before testing Stan.

If the connection does not appear automatically after saving `mcp.json`, reload the VS Code window and reopen the MCP view.

Two deployment modes are supported:

### Remote MCP Server (recommended)

The Remote (HTTP) MCP Server is the recommended path. It eliminates the Node.js/npx dependency, uses streamable HTTP transport, and authenticates through VS Code's sign-in context.

**Configuration** (`.vscode/mcp.json`):

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

**Auth**: VS Code OAuth — transparent, no PAT management needed.

**Turn on the connection**:

1. Save `.vscode/mcp.json`.
2. Open the MCP view in VS Code.
3. Select `ado-remote-mcp`.
4. Start or enable the connection.
5. Complete the VS Code sign-in flow if prompted.

### Local MCP Server (alternative)

The Local (stdio) MCP Server is available when remote is unavailable or a specific stdio setup is required.

**Configuration** (`.vscode/mcp.json`):

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

**Auth**: PAT via `AZURE_DEVOPS_PAT` environment variable, using `--authentication pat` flag.

**Turn on the connection**:

1. Ensure `AZURE_DEVOPS_PAT` is available in the environment used by VS Code.
2. Save `.vscode/mcp.json`.
3. Open the MCP view in VS Code.
4. Select `ado`.
5. Start or enable the connection.
6. Confirm the `core` and `wiki` domains load successfully.

## Domain Filtering

The MCP configuration uses `-d core,wiki` to load only the tool domains Stan needs. This reduces context overhead:
- `core` — essential base tools
- `wiki` — wiki read and search tools

## MCP Wiki Tools

| MCP Tool | Action | Purpose |
|---|---|---|
| `wiki` | `list_wikis` | List all wikis in an org/project |
| `wiki` | `get_wiki` | Get wiki details (by ID or name) |
| `wiki` | `list_pages` | List pages in a wiki hierarchy |
| `wiki` | `get_page` | Get wiki page metadata (path, title, without content body) |
| `wiki` | `get_page_content` | Retrieve full wiki page content body |
| `mcp_ado_search_wiki` | — | Search wiki pages by keyword |

## Access Pattern

Stan wiki-read behavior uses the MCP tool chain:

1. Discover wiki(s) using `wiki list_wikis` or `wiki get_wiki`.
2. List pages using `wiki list_pages` to resolve topic-to-page mappings.
3. Retrieve page content using `wiki get_page` + `wiki get_page_content` for known paths.
4. Search using `mcp_ado_search_wiki` for topic-based queries.

## Outcome Mapping

MCP tool results map to contract outcomes:

| MCP Behavior | Contract Outcome |
|---|---|
| Tool returns page content successfully | `success` |
| Tool returns empty/no result for page/topic | `not_found` |
| Tool returns page metadata but empty content | `no_content` |
| MCP Server connection error / timeout | `unavailable` |
| MCP Server returns authorization error | `access_denied` |

## Behavior Contract

Full behavior guarantees (source anchoring, outcome matrix, error handling, follow-up rules) are defined in `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md`.