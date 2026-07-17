# Stan Quick Start

Get Stan running in VS Code with Azure DevOps wiki access through the MCP Server.

## What you get

After setup, you can:

- Ask Stan quarterly strategy questions based on `docs/strategy-playbook.md`.
- Ask Stan wiki-backed questions using the Data Science Pool Azure DevOps wiki.

## Requirements

- VS Code with GitHub Copilot Chat available.
- Access to this repository in VS Code.
- Azure DevOps access to the Data Science Pool wiki.
- MCP support in VS Code.
- One MCP connection mode:
  - Remote MCP (recommended): VS Code sign-in (OAuth).
  - Local MCP (alternative): Node.js with `npx` and a PAT in `AZURE_DEVOPS_PAT`.

## 1) Open the repository

Open this repo folder in VS Code.

## 2) Configure MCP

Create or update `.vscode/mcp.json`.

### Option A: Remote MCP (recommended)

Use this configuration:

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

Notes:

- No Node.js or PAT management required.
- Uses VS Code sign-in.

### Option B: Local MCP (alternative)

Use this configuration:

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

Notes:

- Requires Node.js and `npx`.
- Set `AZURE_DEVOPS_PAT` in the environment used by VS Code.

## 3) Start the MCP connection in VS Code

- Save `.vscode/mcp.json`.
- Open the MCP view in VS Code. (Shift+Cmd+P / Ctrl+Shift+P → "MCP: List Servers")
- Start or enable your server connection (`ado-remote-mcp` or `ado`).
- If prompted, complete sign-in.
- Confirm the connection status is connected by opening the MCP view again.
- Confirm wiki tools are available.

If the server does not appear, reload the VS Code window and open the MCP view again.

## 4) Run a first-use check

In VS Code, open the Copilot Chat view and run these prompts in the chat input:

- Open Copilot Chat from the Activity Bar, or use Command Palette and run "Chat: Open Chat".
- Start a new chat session.
- If needed, select the Stan agent/mode in chat before sending prompts.

Ask Stan these prompts:

1. `What are the 7 sections of the quarterly strategy session?`
2. `Summarize our DevOps wiki topic on quarterly preparation.`
3. `Which source did you use?`

Expected:

- Prompt 1 follows the seven-section structure in `docs/strategy-playbook.md`.
- Prompt 2 returns wiki-derived content through MCP.
- Prompt 3 states the source is the Data Science Pool Azure DevOps wiki.

## 5) Known scope and behavior

- Wiki retrieval is read-only.
- This setup is wiki-only for Azure DevOps content.
- Requests for Boards, Repos, or Pipelines should return a scope-limit response.

## Troubleshooting

### MCP unavailable

Symptom:

- Stan says wiki content is temporarily unavailable.

Checks:

- MCP connection is started in the MCP view.
- Network access to Azure DevOps is available.
- For local mode, verify Node.js, `npx`, and `AZURE_DEVOPS_PAT`.

### Access denied

Symptom:

- Stan indicates restricted access to the requested page/topic.

Checks:

- Confirm your account has read permission to the target wiki/page.
- Request access from the wiki owner/admin if needed.

### Not found or no content

Symptom:

- Stan says page/topic was not found, or page has no readable content.

Checks:

- Refine page path/topic wording.
- Try a nearby known page or broader keyword.

## References

- Runtime access guide: `docs/stan-agent/devops-access.md`
- Behavior contract: `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md`
- Validation scenarios: `specs/003-mcp-wiki-access/quickstart.md`
