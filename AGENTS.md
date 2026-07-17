# AGENTS.md

## Repo Scope

This repo is a documentation workspace for Stan, the Strategy Assistant for the Data Science Pool.

Primary sources:

- `README.md` for repo purpose and navigation
- `docs/strategy-playbook.md` for the core strategy cadence and session structure
- `.github/copilot-instructions.md` for active Stan behavior guardrails
- `specs/003-mcp-wiki-access/contracts/wiki-read-contract.md` for wiki read behavior contracts

## Working Rules

- Keep changes small and focused.
- Prefer Markdown edits over adding tooling or code.
- Preserve the existing Dutch/English terminology used in the strategy docs.
- Keep links relative and stable.
- Update `README.md` when adding new top-level docs or changing repo structure.

## Editing Guidance

- Treat the strategy playbook as the source of truth for quarterly session content.
- Treat wiki-read behavior and source attribution rules as additive guardrails for Stan responses.
- When revising guidance, keep it practical, decision-focused, and lightweight.
- Avoid inventing process that is not already supported by the current docs.
- If you add a new document, place it under `docs/` unless there is a strong reason not to.

## Stan Scope Guardrails

- Stan is English-first for v1 responses.
- Stan is scoped to quarterly strategy topics in `docs/strategy-playbook.md`.
- For out-of-scope prompts, provide a short scope-limit statement and redirect to supported quarterly topics.
- For annual mission prompts, provide at most one sentence of context, then redirect.

## Wiki Read Guardrails

- Stan can use the Data Science Pool Azure DevOps wiki as a read-only source.
- If asked which source was used, explicitly cite the Data Science Pool Azure DevOps wiki.
- When available, include the resolved wiki page title or path in source attribution.
- For non-wiki Azure DevOps asks (Boards, Repos, Pipelines), return a wiki-only scope-limit notice.

## Validation

- For documentation changes, do a quick consistency check across linked files.
- Verify Markdown links after edits.

## For Future Agents

- Read `README.md`, `docs/strategy-playbook.md`, and `.github/copilot-instructions.md` before making substantive edits.
- If a request conflicts with these docs, update the docs together with the change or call out the mismatch.