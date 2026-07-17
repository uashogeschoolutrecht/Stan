# DevOps Wiki Access

## Purpose

Describe how Stan can read Azure DevOps wiki data at runtime for wiki-backed answers.

## Scope

- Read-only access to Azure DevOps wiki content.
- No write/update operations.
- No Boards/Repos/Pipelines access as part of this capability.

## Required Configuration

Set these values before runtime checks or integration tests:

- Azure DevOps organization URL
- Project name
- Wiki name
- PAT secret in environment variable `AZURE_DEVOPS_PAT`

Example values used in validation:

- Org: `https://dev.azure.com/HogeschoolUtrecht/`
- Project: `Data Science Pool`
- Wiki: `Data-Science-Pool.wiki`

## Authentication

- Auth method: PAT via Basic auth header.
- Secret handling: PAT is stored in `.env` locally as `AZURE_DEVOPS_PAT`.
- Runtime loading pattern: load `AZURE_DEVOPS_PAT` into process environment.

## API Access Pattern

Stan wiki-read behavior uses Azure DevOps Wiki REST APIs:

1. Resolve wiki by org/project.
2. Retrieve page metadata and optionally content by path or page id.
3. Map outcomes to contract statuses:
   - `success`
   - `not_found`
   - `no_content`
   - `unavailable`
   - `access_denied`

## API Response Reference

Concrete response shapes from the Azure DevOps Wiki REST API. These let Stan predict response structure without trial-and-error.

### Endpoint: List wikis

```
GET {org}/{project}/_apis/wiki/wikis?api-version=7.0
```

```json
{
  "value": [
    {
      "id": "e9cd3348-dc0c-4cf9-8921-ae2d0d7a2d78",
      "name": "Data-Science-Pool.wiki",
      "type": "projectWiki",
      "projectId": "63c0199a-9442-4f4e-9679-e983b253b63c",
      "repositoryId": "e9cd3348-dc0c-4cf9-8921-ae2d0d7a2d78",
      "mappedPath": "/"
    }
  ],
  "count": 1
}
```

Key fields: `id` (wiki GUID for subsequent calls), `name`, `type` (`projectWiki`).

### Endpoint: Get single page (by path, no content)

```
GET {org}/{project}/_apis/wiki/wikis/{wikiId}/pages?path=/&api-version=7.0
```

```json
{
  "path": "/",
  "order": 0,
  "isParentPage": true,
  "gitItemPath": "/",
  "subPages": [
    {
      "path": "/Handbook",
      "order": 2147483647,
      "isParentPage": true,
      "gitItemPath": "/Handbook",
      "subPages": [],
      "url": "https://...",
      "remoteUrl": "https://..."
    }
  ],
  "url": "https://...",
  "remoteUrl": "https://...",
  "content": ""
}
```

Without `includeContent=true`, `content` is always `""` and sub-pages are shallow (no nested children).

### Endpoint: Get page WITH content

```
GET {org}/{project}/_apis/wiki/wikis/{wikiId}/pages?path=/Handbook/Communication+strategy&includeContent=true&api-version=7.0
```

```json
{
  "path": "/Handbook/Communication strategy",
  "order": 1,
  "isParentPage": false,
  "gitItemPath": "/Handbook/Communication strategy.md",
  "subPages": [],
  "url": "https://dev.azure.com/...",
  "remoteUrl": "https://...",
  "content": "# Communication strategy\n\n## Purpose\n\nThis page describes how the Data Science Pool communicates...\n\n## Channels\n\n- Teams: ...\n- Email: ...\n\n*(Full markdown body returned in this field)*"
}
```

With `includeContent=true`, `content` contains the full markdown body. `isParentPage=false` means no children.

### Endpoint: Get page by page ID

```
GET {org}/{project}/_apis/wiki/wikis/{wikiId}/pages/{pageId}?includeContent=true&api-version=7.0
```

Response shape is identical to path-based lookup. Useful when the page ID is known from a prior response (e.g., from `subPages` navigation).

### Endpoint: Recursive page tree

```
GET {org}/{project}/_apis/wiki/wikis/{wikiId}/pages?path=/&recursive=true&includeContent=true&api-version=7.0
```

When `recursive=true`, the full page tree is returned as nested `subPages` arrays with `content` populated on every node. This enables a single-call crawl of all wiki pages.

### Not-found response

```
Status: 404 Not Found
```

When the requested page path or ID does not exist, the API returns **HTTP 404** with no JSON body. There is no `not_found` status in the response envelope — detection is purely via HTTP status code.

### No-content scenario

Some pages return `content: ""` even with `includeContent=true` (e.g., parent/index pages with no markdown body but with `subPages` children). Treat this as `no_content` — the page exists but has no readable content.

### Recursive crawl pattern

Use this PowerShell pattern to discover all content-rich pages:

```powershell
function Get-WikiPages($path) {
    $url = "{org}/{project}/_apis/wiki/wikis/{wikiId}/pages" +
           "?path=$([System.Uri]::EscapeDataString($path))" +
           "&includeContent=true&api-version=7.0"
    $page = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    $page  # return current page
    foreach ($sub in $page.subPages) {
        Get-WikiPages $sub.path  # recurse into children
    }
}
```

Leaves with `content.Length > 0` are content-rich pages. Leaves with `subPages.Count = 0` but `content.Length = 0` are empty pages (`no_content`).

### Outcome-to-response mapping

| Outcome | HTTP Status | Response Shape | Stan Action |
|---|---|---|---|
| `success` | 200 | Page JSON with `content.length > 0` | Use `content` as answer source |
| `not_found` | 404 | No JSON body | State page not found, suggest refinement |
| `no_content` | 200 | Page JSON with `content.length = 0`, no subPages | State page exists but empty, suggest adjacent topic |
| `unavailable` | Connection error / timeout | N/A | State temporary unavailability, suggest retry |
| `access_denied` | 401 / 403 | Error body | State restricted access, suggest requesting access |

## Runtime Expectations

- When users ask wiki-backed questions, responses should be derived from readable wiki content.
- When users ask for source, response should mention Azure DevOps wiki source and page/path when available.
- For follow-up prompts, use prior resolved page/topic context.

## Validation References

- Contract: [../../specs/002-read-devops-wiki/contracts/wiki-read-contract.md](../../specs/002-read-devops-wiki/contracts/wiki-read-contract.md)
- Quickstart scenarios: [../../specs/002-read-devops-wiki/quickstart.md](../../specs/002-read-devops-wiki/quickstart.md)
- Run log: [../../specs/002-read-devops-wiki/validation/quickstart-run.md](../../specs/002-read-devops-wiki/validation/quickstart-run.md)

## Known Gaps

- Access-denied validation requires a truly restricted page/account pair.
- Source-citation behavior in Stan runtime must cite wiki source for wiki-backed answers.