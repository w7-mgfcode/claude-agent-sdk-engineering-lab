# Movement 01 — Live SDK Calibration & Evidence Artifact Generation

## Objective

Transition the repository from a scaffolded starting state to verified, evidence-backed proof of Claude Agent SDK execution on the pinned version (`claude-agent-sdk==0.2.134`).

---

## Prerequisites

- Active authentication context for Claude Agent SDK / Claude Code.
- Clean virtual environment synced via `uv sync --all-groups`.

---

## Detailed Execution Steps

### 1. Execute & Verify Example 01 (Stateless Query)
- Run `uv run python examples/01_simple_query.py "Explain asyncio.gather vs TaskGroup in three bullets."`.
- Verify message output, turn completion, and error-free execution.
- Capture execution timing and sanitized terminal output.

### 2. Execute & Verify Example 02 (Interactive CLI & Session Resume)
- Run `uv run python examples/02_terminal_cli.py`.
- Conduct a 2-turn dialogue verifying context retention.
- Inspect `.claude_agent_lab/sessions.json` for written session metadata.
- Quit and re-run with `--resume last`. Verify that conversation state is restored.
- Document any SDK subtleties or latency characteristics.

### 3. Execute & Verify Example 04 (Custom In-Process MCP Tool)
- Run `uv run python examples/04_tool_use.py`.
- Verify that the model triggers `get_project_facts` via the in-process MCP server.
- Confirm input validation and narrow `allowed_tools` filtering.

### 4. Execute & Verify Example 05 (PreToolUse Hook)
- Run `uv run python examples/05_permission_hook.py`.
- Verify deterministic policy decision logging for both allowed and denied tool use attempts.

### 5. Run Live Smoke Test Suite
- Run `RUN_LIVE_CLAUDE_TESTS=1 uv run pytest -m live tests/live/test_sdk_smoke.py`.
- Confirm live test passes cleanly without regressions.

---

## Artifact Updates & Documentation

- Update [docs/EVIDENCE.md](../EVIDENCE.md) with verified sample outputs and test confirmation.
- Update [docs/DEMO_SCRIPT.md](../DEMO_SCRIPT.md) with realistic execution logs.
- Record any observed quirks or troubleshooting steps in [docs/TROUBLESHOOTING.md](../TROUBLESHOOTING.md).

---

## Definition of Done

- [ ] All 5 example scripts run successfully against the live SDK.
- [ ] `tests/live/test_sdk_smoke.py` passes with `RUN_LIVE_CLAUDE_TESTS=1`.
- [ ] `docs/EVIDENCE.md` contains zero unverified claims.
- [ ] `make verify` passes with exit code 0.
