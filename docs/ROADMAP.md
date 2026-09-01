# Development Roadmap

The starter ZIP is intentionally a strong first commit. Recommended implementation/hardening order:

## M0 — Bootstrap

- [ ] Create public GitHub repo and push starter.
- [ ] Run `uv lock` / `uv sync --all-groups` on your development machine.
- [ ] Run `make verify` and fix any SDK-version-specific typing drift.
- [ ] Confirm CI passes on GitHub.

## M1 — Live one-shot evidence

- [ ] Authenticate Claude Agent SDK locally.
- [ ] Run Example 01.
- [ ] Add a sanitized sample output to README.
- [ ] Run the live smoke test.

## M2 — Stateful client

- [ ] Perform a two-turn CLI conversation.
- [ ] Verify `session_id` is persisted.
- [ ] Restart with `--resume last` and verify behavior on the pinned SDK.
- [ ] Document any SDK caveat rather than masking it.

## M3 — Tool evidence

- [ ] Run Example 04 and verify the MCP tool is actually invoked.
- [ ] Add one test around the tool's deterministic domain logic.
- [ ] Capture a sanitized tool-call demonstration.

## M4 — API boundary

- [ ] Start FastAPI locally.
- [ ] Verify `/health`.
- [ ] Make one live `/v1/chat/completions` call.
- [ ] Add HTTP success/error examples to README.

## M5 — Hiring-manager polish

- [ ] Add architecture screenshot or short GIF only if it adds evidence.
- [ ] Add CI badge after first successful workflow run.
- [ ] Link this repo from CV/LinkedIn/GitHub profile.
- [ ] Re-audit `docs/EVIDENCE.md` line by line.

## Optional later extensions

Only after v1 is verified:

- server-sent-event streaming with clean disconnect cancellation;
- Agent SDK hooks demonstrating deterministic PreToolUse policy;
- OpenTelemetry if stable on the pinned SDK;
- containerized local run.

Do not add RAG/vector DB/multi-agent complexity merely to increase repository size.
