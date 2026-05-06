# OpenCode Foreman Crew Template

A locally generated, safer OpenCode multi-agent template inspired by `1ilkhamov/opencode-hermes-multiagent`, tailored for Bill/Karl workflow.

This is not installed automatically. It is a mergeable template.

## Design

- Primary orchestrator: `foreman`
- Models use your existing OpenCode providers:
  - primary: `ollama/kimi-k2.5`
  - subagents: `ollama/glm-5.1`
- No third-party plugin entries.
- No package install required.
- Tool isolation:
  - orchestrator: task/todos only
  - scout/analyst/reviewer/security: read-only
  - coder/fixer/refactorer/tester/devops: scoped write/bash where needed

## Files

- `opencode.foreman-crew.json` — mergeable OpenCode agent config fragment/template
- `agent/core/foreman.md` — primary orchestrator prompt
- `agent/subagents/**.md` — specialized subagent prompts
- `scripts/merge_opencode_config.py` — creates a backed-up merged config

## Safe install preview

```bash
python3 scripts/merge_opencode_config.py --dry-run
```

## Install into live OpenCode config

```bash
python3 scripts/merge_opencode_config.py --apply
```

The script backs up `~/.config/opencode/opencode.json` first.

## Test in a disposable repo first

```bash
mkdir -p /tmp/karl-crew-smoke && cd /tmp/karl-crew-smoke
git init
printf 'console.log("hello")
' > index.js
opencode run --agent foreman 'Inspect this tiny repo and report the test/build commands. Do not modify files.'
```
