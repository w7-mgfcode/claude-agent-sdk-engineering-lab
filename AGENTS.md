# AGENTS.md

## Mission

Develop this repository as an evidence-first Claude Agent SDK portfolio project. Prefer small, inspectable, testable changes over feature breadth.

## Non-negotiable rules

1. Do not claim a feature in README/EVIDENCE until concrete source code and a test or manual verification path exist.
2. Keep `claude-agent-sdk` usage explicit; do not hide all SDK calls behind abstractions.
3. No secrets, API keys, session credentials, or private transcripts in Git.
4. Do not enable Bash, unrestricted filesystem writes, or dangerous permission modes by default.
5. Live Claude calls must remain opt-in in tests.
6. Preserve the distinction between Claude Agent SDK application development and merely using Claude/Codex as coding assistants.
7. Keep the OpenAI compatibility claim limited to the implemented request/response subset.

## Quality gate

Before a PR is considered complete:

```bash
make verify
```

For changes to live SDK behavior, also perform the relevant manual smoke test and record the result in the PR description.
