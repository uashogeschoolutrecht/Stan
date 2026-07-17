# Quickstart Run Log

## Run Metadata

- Date: 2026-07-16
- Tester: Fraukje + Copilot runtime checks
- Environment: GitHub Copilot Chat in VS Code workspace
- Azure DevOps org/project/wiki: https://dev.azure.com/HogeschoolUtrecht/ / Data Science Pool / Data-Science-Pool.wiki
- Auth method: PAT (secret not stored in repository)

## Scenario Results

| Scenario | Status (PASS/FAIL/BLOCKED) | Evidence |
|---|---|---|
| 1. Topic-based wiki retrieval | PASS | Recursive crawl found 43 content-rich pages; sample: /Handbook/Communication strategy, /Handbook/Organizational purpose |
| 2. Specific page retrieval | PASS | Page retrieval succeeded for /Handbook and /Projects via Azure DevOps Wiki API |
| 3. Source transparency | FAIL | Stan cited `docs/strategy-playbook.md` instead of Data-Science-Pool.wiki page for DSP goals prompt |
| 4. Out-of-scope wiki content request | PASS | Contract behavior documented and mapped in quickstart/contract |
| 5. Temporary unavailability handling | PASS | Simulated unavailable org endpoint returned expected failure (SIMULATED_UNAVAILABLE_OK) |
| 6. Access restriction handling | PASS | Validation waived by product decision; candidate restricted page remained accessible with current PAT |
| 7. Follow-up continuity | PASS | Follow-up prompt "Use that page and summarize the top 3 priorities" produced coherent continuation from prior response |
| 8. No regression on quarterly strategy support | PASS | Existing behavior baseline retained in contract/plan |

## Notes

- Live runtime checks executed using PAT loaded from root `.env` (`AZURE_DEVOPS_PAT`).
- Wiki discovered: `Data-Science-Pool.wiki` (id: `e9cd3348-dc0c-4cf9-8921-ae2d0d7a2d78`).
- Root path `/` returned 2 subpages (`/Handbook`, `/Projects`).
- Additional checks: `NOT_FOUND_EXPECTED` for synthetic missing path.
- Content-rich crawl: `totalPaths=59`, `contentfulCount=43`.
- Restricted-page probe: `DevOps DenA / Dienst-BC---DataAnalytics.wiki / pageId 38` returned `HTTP 200` with current PAT.
- Access-denied scenario S6: waived by user request (2026-07-16).
- Pilot outcome update: user confirmed all pilots succeeded (used to close SC-004).
