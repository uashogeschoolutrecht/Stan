# Implementation Plan: Azure DevOps MCP Wiki Access

**Branch**: `003-mcp-wiki-access` | **Date**: 2026-07-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-mcp-wiki-access/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command; its definition describes the execution workflow.

## Summary

Replace the REST API-based wiki read path in Stan with the Azure DevOps MCP Server (VS Code MCP Extension). All existing wiki-read behavior contracts (source boundaries, outcome matrix, error handling) are preserved; only the transport mechanism changes. The REST wiki-read code in Stan's instruction files and `docs/stan-agent/devops-access.md` is removed entirely — no fallback or dual-path is retained.

## Technical Context

**Language/Version**: Markdown + YAML-frontmatter instruction files (Copilot agent customization)

**Primary Dependencies**: Azure DevOps MCP Server VS Code Extension, VS Code MCP Extension configuration (`mcp.json`), Stan agent `.github/copilot-instructions.md`

**Storage**: N/A — wiki content is accessed at runtime through MCP tool calls; no local persistence

**Testing**: Manual scenario-based validation via quickstart prompts mapped to contract vectors

**Target Platform**: VS Code Copilot Chat with Stan agent configuration in this repository context

**Project Type**: Copilot agent behavior documentation + MCP server configuration

**Performance Goals**: Functional equivalence with REST-based path (speed is a side benefit per spec clarification)

**Constraints**: Documentation-first, no new runtime tooling beyond MCP extension config, remove REST wiki-read code entirely, preserve existing quarterly strategy behavior, reuse existing DevOps PAT for MCP auth, stable relative links

**Scale/Scope**: Single Azure DevOps wiki, single MCP Server connection, read-only scope

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Article I: Source of Truth** - PASS. Quarterly strategy facts remain anchored to `docs/strategy-playbook.md`; wiki scope is bounded to Data Science Pool Azure DevOps wiki. The transport mechanism change does not affect source-of-truth hierarchy.
- **Article II: Documentation First** - PASS. All outputs are markdown artifacts (plan, research, data model, contract, quickstart). No code or tooling is introduced beyond the MCP configuration documentation.
- **Article III: Stable Language and Links** - PASS. Existing terminology preserved. Contract references in repo-scoped instruction files will be updated to the new 003 spec paths.
- **Article IV: Repo Hygiene** - PASS. `.github/copilot-instructions.md` and `docs/stan-agent/devops-access.md` will be updated to reflect the new MCP-based wiki access method. README.md may be touched if the specs listing changes.
- **Article V: Spec Kit Alignment** - PASS. Plan follows Spec Kit phase outputs (research, data model, contracts, quickstart).
- **Article VI: Minimal Tooling** - PASS. No new tooling or automation added. The MCP server configuration is an external dependency documented in guidance files.

Post-Phase 1 re-check: PENDING (re-evaluated after design artifacts are complete).

## Project Structure

### Documentation (this feature)

```text
specs/003-mcp-wiki-access/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — MCP Server capabilities research
├── data-model.md        # Phase 1 output — entities adapted from 002 with MCP transport
├── quickstart.md        # Phase 1 output — validation scenarios
├── contracts/           # Phase 1 output — updated wiki-read contract
│   └── wiki-read-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created by /speckit.plan)
```

### Source Code (repository root)

The repo is documentation-only. This feature touches the following existing files:

```text
.github/
└── copilot-instructions.md   # UPDATE: point wiki-read contract to 003 path

docs/
├── strategy-playbook.md      # UNCHANGED
└── stan-agent/
    └── devops-access.md      # REWRITE: REST API docs → MCP Server docs

specs/
├── 001-stan-chat-agent/
├── 002-read-devops-wiki/     # RETAINED: historical artifacts (superseded)
└── 003-mcp-wiki-access/      # THIS FEATURE
```

**Structure Decision**: Documentation-only repo; no project source tree to define. The feature produces new artifacts under `specs/003-mcp-wiki-access/` and updates two existing repo-root files (copilot-instructions.md, stan-agent/devops-access.md).

## Complexity Tracking

No constitution violations — all six articles pass. Complexity tracking is not required.
