# Starter Status

This ZIP is a **development starting point**, not evidence of live SDK execution by itself.

## Already scaffolded

- direct `claude_agent_sdk.query()` runtime path;
- direct `ClaudeSDKClient` interactive path;
- SDK MCP custom tool registration;
- FastAPI compatibility subset;
- dependency-injected fake gateway tests;
- credential-free unit/integration test structure;
- CI, security, architecture, PRD and evidence documentation.

## Verified in the build environment

- all Python files compile;
- credential-free tests pass against a minimal SDK interface stub;
- API contract tests pass with the fake gateway.

## Must be verified on your development machine before claiming completion

1. `uv sync --all-groups` and commit the generated `uv.lock`.
2. `make verify` against the real pinned dependencies.
3. Run Example 01 with real Claude Agent SDK authentication.
4. Run a two-turn Example 02 session and verify `--resume last`.
5. Run Example 04 and confirm the custom MCP tool is invoked.
6. Run one live FastAPI request.
7. Update README sample output / EVIDENCE only with observed results.

This boundary is intentional: a skill repository should make claims only after the corresponding behavior has been executed and verified.
