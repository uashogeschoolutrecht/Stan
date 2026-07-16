# Spec Kit Setup for Stan

This repository is documentation-first, so the Spec Kit setup is intentionally lightweight.

## What is set up here

- Copilot context: [.github/copilot-instructions.md](../.github/copilot-instructions.md)
- Copilot command files: [.github/agents/](../.github/agents/)
- Copilot prompt wrappers: [.github/prompts/](../.github/prompts/)
- Project constitution: [.specify/memory/constitution.md](../.specify/memory/constitution.md)
- Strategy source of truth: [strategy-playbook.md](strategy-playbook.md)

## How to use Spec Kit in this repo

1. Install Spec Kit with `specify-cli`.
2. Initialize the repo with the Copilot integration.
3. Keep generated spec, plan, and task artifacts aligned with the strategy playbook.
4. Use the constitution as the guardrail for any future Spec Kit-driven work.

## Recommended Windows command

```powershell
specify init Stan --integration copilot --script ps
```

If you already have Spec Kit installed, use the generated `/speckit.*` commands from your agent workflow and keep the outputs in sync with the docs here.

## Notes

- Keep any Spec Kit artifacts under `.specify/`.
- Keep the repo's existing documentation structure intact.
- Update this setup note if the strategy workflow changes.