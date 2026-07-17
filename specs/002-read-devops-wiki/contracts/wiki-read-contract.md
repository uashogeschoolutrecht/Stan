# Chat Behavior Contract: Stan Azure DevOps Wiki Read (v1)

## Purpose

Define user-visible behavior guarantees for Stan when answering with Data Science Pool Azure DevOps wiki content.

## Scope

- In scope:
  - Read-only retrieval from Data Science Pool Azure DevOps wiki.
  - Topic/page-based wiki question answering.
  - Follow-up questions about previously retrieved wiki information.
  - Explicit handling of not-found, unavailable, and access-denied outcomes.
- Out of scope:
  - Writing or editing wiki pages.
  - Accessing Azure DevOps artifacts other than the wiki.
  - Replacing existing quarterly strategy behavior.

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
| unavailable | Wiki is temporarily unavailable | Suggest retry later |
| access_denied | Access is restricted | Suggest requesting access |

## Response Behavior Rules

### Successful wiki retrieval

- Stan MUST provide a relevant answer derived from retrieved wiki content.
- Stan SHOULD align wording with the user request while preserving wiki meaning.

### Topic-based retrieval

- Stan MUST resolve topic-style prompts to the most relevant wiki page(s) in scope.
- Stan MUST summarize retrieved topic content before optional detail expansion.

### Page-specific retrieval

- Stan MUST honor explicit page hints/path when supplied by the user.
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

- Stan MUST state that wiki content is currently unavailable.
- Stan SHOULD suggest retrying later.
- Stan SHOULD avoid presenting stale content as current when unavailable.

### Access restricted

- Stan MUST state that wiki access is restricted for the requested page/topic.
- Stan SHOULD suggest requesting access from the wiki owner/admin.
- Stan MUST avoid implying missing page when the condition is permission-related.

### Follow-up queries

- Stan MUST support follow-up questions using conversation context from the most recently retrieved wiki topic/page.
- Stan MUST ask for clarification when follow-up intent cannot be resolved from context.

## Acceptance Test Vectors

1. Prompt: "What does our DevOps wiki say about quarterly prep?"
   - Expected: Relevant summary derived from wiki content.
2. Prompt: "Which source did you use?"
   - Expected: States Data Science Pool Azure DevOps wiki as source.
3. Prompt: "Open wiki page X that I do not have access to."
   - Expected: Clear access-restricted message and request-access suggestion.
4. Prompt: "Get wiki page Y" when service is down.
   - Expected: Clear unavailable message and retry guidance.
5. Prompt: "Use the previous page and explain the decision points."
   - Expected: Follow-up answer uses prior retrieved page context.
6. Prompt: "Also read boards and pipelines for this."
   - Expected: Scope-limit note that this feature is wiki-only.
7. Prompt: "Summarize our wiki topic on quarterly preparation."
   - Expected: Topic-based wiki summary from relevant page content.
8. Prompt: "Use page /Strategy/Quarterly-Prep and list key decisions."
   - Expected: Response aligned to that page content and decision points.

## Versioning

- Contract version: `v1`
- Compatibility note: Expanding beyond wiki read-only scope MUST bump contract version and add vectors.
