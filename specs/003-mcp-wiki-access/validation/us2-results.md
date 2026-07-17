# US2 Validation Results — More Accurate and Reliably Sourced Wiki-Backed Answers

**Goal**: Stan's wiki responses are correctly scoped to wiki-only content with proper source attribution

**Linked requirements**: FR-004, FR-005, FR-009, FR-010, SC-002

**Date**: 2026-07-17
**Tester**:

---

## Scenario S3: Source transparency

| Step | Action | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | After a wiki-derived answer, ask "Where did that info come from?" | Response identifies Data Science Pool Azure DevOps wiki | | ☐ Pass ☐ Fail |
| 2 | Verify response includes page/topic reference when available | Page title or path included | | ☐ Pass ☐ Fail |

**Outcome**: ☐ Pass ☐ Fail
**Notes**:

---

## Scenario S4: Out-of-scope wiki content request

| Step | Action | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | Ask for non-wiki content (e.g., "List my work items") | Stan does NOT use non-wiki MCP tools | | ☐ Pass ☐ Fail |
| 2 | Verify response states scope limitation | Response says wiki-only | | ☐ Pass ☐ Fail |

**Outcome**: ☐ Pass ☐ Fail
**Notes**:

---

## Scenario S7: Follow-up continuity

| Step | Action | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | Ask Stan for a known wiki topic | Initial answer returned | | ☐ Pass ☐ Fail |
| 2 | Ask follow-up referring to "that page" or "the previous topic" | Uses prior context | | ☐ Pass ☐ Fail |
| 3 | If ambiguous, verify Stan asks for clarification | Clarification asked | | ☐ Pass ☐ Fail |

**Outcome**: ☐ Pass ☐ Fail
**Notes**:

---

## Scenario S8: No regression on quarterly strategy support

| Step | Action | Expected | Actual | Pass/Fail |
|------|--------|----------|--------|-----------|
| 1 | Ask quarterly strategy question (e.g., "What are the 7 sections?") | Response follows existing playbook behavior | | ☐ Pass ☐ Fail |

**Outcome**: ☐ Pass ☐ Fail
**Notes**:

---

## Summary

| Scenario | Result | FR Coverage |
|----------|--------|-------------|
| S3 | ☐ Pass ☐ Fail | FR-010 |
| S4 | ☐ Pass ☐ Fail | FR-004 |
| S7 | ☐ Pass ☐ Fail | FR-009 |
| S8 | ☐ Pass ☐ Fail | FR-005 |
| **US2 Overall** | ☐ Pass ☐ Fail | |
