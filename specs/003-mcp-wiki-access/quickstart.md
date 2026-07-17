# Quickstart Validation Guide: Azure DevOps MCP Wiki Access

## Prerequisites

- Feature artifacts exist in `specs/003-mcp-wiki-access/`.
- Specification is available at `specs/003-mcp-wiki-access/spec.md`.
- Contract is available at `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md`.
- Azure DevOps MCP Server is configured in `.vscode/mcp.json` (see [configuration reference](contracts/wiki-read-contract.md#configuration-reference) and `docs/stan-agent/devops-access.md`).
- The Azure DevOps MCP connection has been enabled in the VS Code MCP view and shows as connected.
- Access to Data Science Pool Azure DevOps wiki is configured for the authenticated user.

## Requirement Traceability

| Requirement | Quickstart Scenario(s) |
|---|---|
| FR-001 | S1 |
| FR-002 | S1, S2 |
| FR-003 | S1, S2 |
| FR-004 | S4 |
| FR-005 | S8 |
| FR-006 | S5 |
| FR-007 | S6 |
| FR-008 | S10 |
| FR-009 | S3, S4, S7 |
| FR-010 | S3 |
| FR-011 | S9 |

## Validation Scenario S1: Topic-based wiki retrieval (MCP path)

1. Ensure Azure DevOps MCP Server is running and the `wiki` domain is loaded.
2. Ask Stan for a known Data Science Pool wiki topic.
3. Verify Stan calls the appropriate MCP wiki tool (e.g., `mcp_ado_search_wiki` or `wiki get_page_content`).
4. Verify response includes relevant wiki-derived information.
5. Expected outcome:
   - Meets `FR-001`, `FR-002`, and `FR-003`.
   - Content is retrieved through MCP Server, not REST API.

## Validation Scenario S2: Specific page retrieval (MCP path)

1. Ask Stan for details from a specific known wiki page (e.g., by path).
2. Verify Stan uses `wiki get_page` + `wiki get_page_content` MCP tools.
3. Verify response aligns with that page content.
4. Expected outcome:
   - Meets `FR-002` and `FR-003`.

## Validation Scenario S3: Source transparency

1. After a wiki-derived answer, ask Stan where the information came from.
2. Verify response identifies Data Science Pool Azure DevOps wiki.
3. Verify response includes page/topic reference when available.
4. Expected outcome:
   - Meets `FR-010` and contract source rules.

## Validation Scenario S4: Out-of-scope wiki content request

1. Ask for content not covered in available wiki scope (e.g., "List my work items").
2. Verify Stan does NOT use non-wiki MCP tools.
3. Verify response states scope limitation.
4. Expected outcome:
   - Meets `FR-004`.

## Validation Scenario S5: Temporary unavailability handling

1. Simulate MCP Server unavailability (e.g., stop the MCP Server or disconnect the network).
2. Ask a wiki-based question.
3. Verify response clearly states temporary unavailability through the MCP Server.
4. Expected outcome:
   - Meets `FR-006` and `SC-003`.
5. Simulation note:
   - Stop the MCP Server from the VS Code MCP view, or disconnect the remote MCP URL.

## Validation Scenario S6: Access restriction handling

1. Ask for a page/topic without read permission.
2. Verify Stan returns a clear access-restricted message.
3. Verify response suggests requesting access.
4. Expected outcome:
   - Meets `FR-007` and `SC-003`.
5. Simulation note:
   - Use a wiki page on a project the authenticated user does not have access to.

## Validation Scenario S7: Follow-up continuity

1. Ask Stan for a known wiki topic.
2. Ask a follow-up question referring to "that page" or "the previous topic".
3. Verify response uses prior context or asks clarification if ambiguous.
4. Expected outcome:
   - Meets `FR-009`.

## Validation Scenario S8: No regression on quarterly strategy support

1. Ask an existing quarterly strategy structure question (e.g., "What are the 7 sections of the quarterly strategy session?").
2. Verify response remains correct and follows existing behavior from `docs/strategy-playbook.md`.
3. Expected outcome:
   - Meets `FR-005`.

## Validation Scenario S9: REST code removal

1. Verify that no references to REST API wiki endpoints remain in Stan's active instruction files.
2. Verify `.github/copilot-instructions.md` references `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md`, not the 002 path.
3. Verify `docs/stan-agent/devops-access.md` describes MCP Server configuration, not REST API patterns.
4. Expected outcome:
   - Meets `FR-011`.

## Validation Scenario S10: Not-found and no-content handling

1. Ask Stan for a wiki page that does not exist (e.g., a made-up page path).
2. Verify Stan states the requested page/topic could not be found.
3. Verify Stan suggests a nearby page name or topic refinement.
4. Ask Stan for a wiki page that exists but has no readable content (if such a page is available).
5. Verify Stan states the page exists but has no readable content.
6. Verify Stan suggests an adjacent page/topic.
7. Expected outcome:
   - Meets `FR-008` and `SC-003`.
8. Simulation note:
   - For not-found: request a page path that does not exist in the wiki hierarchy.
   - For no-content: use a wiki page that exists but is empty or has minimal content.

## Exit Criteria

- All ten scenarios pass.
- Error messages are deterministic for unavailable/restricted/not-found cases.
- Existing quarterly strategy guidance remains intact.
- No REST API wiki-read code or configuration remains in active documentation.
