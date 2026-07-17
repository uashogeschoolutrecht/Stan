# Quickstart Validation Guide: Read Azure DevOps Wiki

## Prerequisites

- Feature artifacts exist in `specs/002-read-devops-wiki/`.
- Specification is available at `specs/002-read-devops-wiki/spec.md`.
- Contract is available at `specs/002-read-devops-wiki/contracts/wiki-read-contract.md`.
- Access to Data Science Pool Azure DevOps wiki is configured for test user.

## Requirement Traceability

| Requirement | Quickstart Scenario(s) |
|---|---|
| FR-001 | S1 |
| FR-002 | S1, S2 |
| FR-003 | S1, S2 |
| FR-004 | S4 |
| FR-005 | S5 |
| FR-006 | S6 |
| FR-007 | S7 |
| FR-008 | S8 |
| FR-009 | S3, S4 |

## Validation Scenario S1: Topic-based wiki retrieval

1. Ask Stan for a known Data Science Pool wiki topic.
2. Verify response includes relevant wiki-derived information.
3. Expected outcome:
   - Meets `FR-001`, `FR-002`, and `FR-003`.

## Validation Scenario S2: Specific page retrieval

1. Ask Stan for details from a specific known wiki page.
2. Verify response aligns with that page content.
3. Expected outcome:
   - Meets `FR-002` and `FR-003`.

## Validation Scenario S3: Source transparency

1. After a wiki-derived answer, ask Stan where the information came from.
2. Verify response identifies Data Science Pool Azure DevOps wiki.
3. Verify response includes page/topic reference when available.
4. Expected outcome:
   - Meets user story 2 acceptance and contract source rules.

## Validation Scenario S4: Out-of-scope wiki content request

1. Ask for content not covered in available wiki scope.
2. Verify response states scope limitation.
3. Verify response redirects to wiki topic/page wording.
4. Expected outcome:
   - Meets `FR-004`.

## Validation Scenario S5: Temporary unavailability handling

1. Simulate unavailable wiki access.
2. Ask a wiki-based question.
3. Verify response clearly states temporary unavailability.
4. Expected outcome:
   - Meets `FR-005` and `SC-003`.
5. Simulation note:
   - Example approaches: temporary network block, invalid wiki endpoint, or maintenance window.

## Validation Scenario S6: Access restriction handling

1. Use a page/topic without read permission.
2. Ask Stan to retrieve it.
3. Verify response clearly states restricted access and suggests requesting access.
4. Expected outcome:
   - Meets `FR-006` and `SC-002`.
5. Simulation note:
   - Use a dedicated restricted test page or a least-privilege account.

## Validation Scenario S7: Follow-up continuity

1. Ask Stan for a known wiki topic.
2. Ask a follow-up question referring to "that page" or "the previous topic".
3. Verify response uses prior context or asks clarification if ambiguous.
4. Expected outcome:
   - Meets `FR-007`.

## Validation Scenario S8: No regression on quarterly strategy support

1. Ask an existing quarterly strategy structure question.
2. Verify response remains correct and in line with prior feature behavior.
3. Expected outcome:
   - Meets `FR-008`.

## Exit Criteria

- All eight scenarios pass.
- Error messages are deterministic for unavailable/restricted/not-found cases.
- Existing quarterly strategy guidance remains intact.
