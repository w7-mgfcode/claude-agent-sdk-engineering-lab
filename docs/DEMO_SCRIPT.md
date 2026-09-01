# 5-minute Technical Demo Script

## 0:00–0:45 — Purpose

“This repository is a focused Claude Agent SDK engineering demonstration. I kept it small so the SDK integration, async lifecycle, tool permissions, FastAPI boundary, and tests are visible without digging through a large product.”

## 0:45–1:30 — One-shot

Open `sdk_adapter.py` and `01_simple_query.py`.

Point out:

- `query()`;
- async message iteration;
- `AssistantMessage` / `ResultMessage` handling;
- timeout and cost/turn bounds.

## 1:30–2:30 — Stateful client

Open `02_terminal_cli.py`.

Point out:

- `async with ClaudeSDKClient`;
- `await client.query(...)`;
- `receive_response()`;
- `asyncio.timeout`;
- interrupt on timeout;
- session ID persistence and explicit resume.

## 2:30–3:30 — Tool/MCP

Open `project_facts.py` and `04_tool_use.py`.

Point out:

- `@tool`;
- `create_sdk_mcp_server`;
- one harmless deterministic tool;
- exact `allowed_tools` entry;
- no Bash / bypassPermissions.

## 3:30–4:30 — FastAPI + tests

Open `api.py` and `test_api_fake_sdk.py`.

Point out:

- typed Pydantic contract;
- dependency-injected SDK gateway;
- explicit rejection of unsupported fields;
- timeout to HTTP 504 mapping;
- credential-free tests.

## 4:30–5:00 — Verify

Run:

```bash
make verify
```

If authenticated and appropriate:

```bash
RUN_LIVE_CLAUDE_TESTS=1 uv run pytest -m live tests/live/test_sdk_smoke.py
```
