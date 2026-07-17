# Feature Specification: Azure DevOps MCP Wiki Access

**Feature Branch**: `[003-mcp-wiki-access]`

**Created**: 2026-07-17

**Status**: Draft

**Input**: User description: "Stan now uses REST API to read the wiki but instead I would like Stan to use the Azure DevOps MCP Server. This will streamline the architecture and make Stan's responses faster and more accurate"

## Clarifications

### Session 2026-07-17

- Q: How does Stan authenticate with the Azure DevOps MCP Server? → A: Uses the same DevOps PAT (Personal Access Token) from environment/config as the current REST-based path.
- Q: How is the Azure DevOps MCP Server deployed/provided to Stan? → A: Via a VS Code MCP Extension installed in the editor, following the standard VS Code MCP integration pattern.
- Q: What happens to the current REST wiki-read code after switching to MCP? → A: Remove the REST wiki-read code entirely — no fallback or dual-path is retained.
- Q: How is the response-time improvement measured for SC-002? → A: Removed SC-002 — speed is a side benefit, success is functional equivalence.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Answer wiki questions through the shared DevOps connection (Priority: P1)

As a Data Science Pool team member, I can ask Stan strategy questions that rely on Azure DevOps wiki content and receive answers through the shared Azure DevOps connection so the information path is more direct and dependable.

**Why this priority**: This preserves the existing wiki-read value while replacing the underlying access path with the intended DevOps connection model.

**Independent Test**: Can be fully tested by asking Stan for a known wiki topic and verifying the response uses current wiki content obtained through the Azure DevOps MCP Server path.

**Acceptance Scenarios**:

1. **Given** a user asks for a topic covered in the Data Science Pool Azure DevOps wiki, **When** Stan responds, **Then** Stan returns a relevant summary derived from accessible wiki content through the Azure DevOps MCP Server.
2. **Given** a user asks for details from a specific wiki page, **When** Stan responds, **Then** Stan includes information consistent with that page and preserves the existing wiki-only scope.

---

### User Story 2 - Provide more accurate and reliably sourced wiki-backed answers (Priority: P2)

As a user, I want Stan's wiki-backed responses to reflect the right source content so I can trust the guidance during strategy preparation.

**Why this priority**: The requested change is justified by more direct and dependable access to wiki content through the MCP Server.

**Independent Test**: Can be fully tested by asking a wiki-backed question and verifying the response uses current MCP-retrieved content and correctly identifies the source as the Data Science Pool Azure DevOps wiki.

**Acceptance Scenarios**:

1. **Given** a user asks a common wiki-backed question, **When** Stan responds after the change, **Then** the answer is derived from current wiki content obtained through the Azure DevOps MCP Server.
2. **Given** a user asks for content from a known wiki page, **When** Stan responds, **Then** the answer reflects the matching page content without mixing in unsupported DevOps areas.

---

### User Story 3 - Fail clearly when the shared DevOps connection is unavailable (Priority: P3)

As a user, I need clear feedback when the Azure DevOps MCP Server path cannot provide wiki content so I know whether to retry, adjust the request, or seek access.

**Why this priority**: A streamlined architecture still needs predictable failure handling to avoid silent degradation or misleading answers.

**Independent Test**: Can be fully tested by simulating unavailable, restricted, and empty wiki results and verifying Stan returns the correct user-facing message in each case.

**Acceptance Scenarios**:

1. **Given** the Azure DevOps MCP Server path is temporarily unavailable, **When** a user asks a wiki-based question, **Then** Stan returns a clear message that wiki content is currently unavailable through the shared DevOps connection.
2. **Given** a user asks for a wiki page they cannot access, **When** Stan attempts to retrieve it, **Then** Stan explains that access is restricted and suggests requesting access.

---

### Edge Cases

- A user asks for a wiki page that does not exist.
- A user asks for a wiki page that exists but has no readable content.
- The Azure DevOps MCP Server can connect to DevOps but cannot return wiki content for the requested page.
- A request mentions Boards, Repos, or Pipelines alongside a wiki question and Stan must answer only the wiki-backed portion.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to ask for information from the Data Science Pool Azure DevOps wiki in natural language.
- **FR-002**: System MUST retrieve accessible wiki content through the Azure DevOps MCP Server instead of the current REST-based wiki read path.
- **FR-003**: System MUST use retrieved wiki content to answer the user's requested topic or page.
- **FR-004**: System MUST preserve Stan's existing wiki-only source boundary for Azure DevOps content.
- **FR-005**: System MUST maintain current quarterly strategy support behavior while replacing the wiki access path.
- **FR-006**: System MUST communicate when requested wiki content cannot be retrieved because the Azure DevOps MCP Server path is temporarily unavailable.
- **FR-007**: System MUST communicate when requested wiki content cannot be retrieved because access is restricted.
- **FR-008**: System MUST communicate when the requested wiki content does not exist or has no readable content.
- **FR-009**: Users MUST be able to ask follow-up questions about wiki information retrieved in the same conversation.
- **FR-010**: System MUST identify the Data Science Pool Azure DevOps wiki as the source when users ask which source was used.
- **FR-011**: System MUST remove the current REST-based wiki read code — no fallback or dual-path is retained once the MCP path is operational.

### Key Entities *(include if feature involves data)*

- **Wiki Query**: A user request for a wiki topic, page, or follow-up detail.
- **Wiki Source Result**: The returned wiki lookup outcome, including successful content, no content, missing page, temporary unavailability, or access restriction.
- **Source Citation**: The user-facing reference that identifies the Data Science Pool Azure DevOps wiki as the information source.
- **DevOps Access Channel**: The approved connection path Stan uses to reach the wiki through the Azure DevOps MCP Server, deployed as a VS Code MCP Extension and authenticated via the existing DevOps PAT from environment/config.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of tested requests for known wiki topics return relevant wiki-derived answers on the first response.
- **SC-002**: At least 95% of tested wiki-backed responses match the expected source page or topic without requiring manual correction.
- **SC-003**: 100% of tested unavailable, missing-page, no-content, and access-restricted cases return the correct user-facing message.

## Assumptions

- The Data Science Pool Azure DevOps wiki remains the only new external content source covered by this feature.
- The Azure DevOps MCP Server is deployed as a VS Code MCP Extension, following the standard VS Code MCP integration pattern used by Copilot extensions.
- Stan authenticates to the Azure DevOps MCP Server using the same DevOps PAT (Personal Access Token) from environment/config that the current REST-based path uses — no new credential infrastructure is introduced.
- This feature replaces the current REST-based wiki retrieval path rather than adding a second parallel wiki source for normal operation.
- Wiki content remains read-only for Stan; editing or writing wiki content is out of scope.
- Existing quarterly strategy guidance in the repository remains authoritative and the wiki source is additive when relevant.