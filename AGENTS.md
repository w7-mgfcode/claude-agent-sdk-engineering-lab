# AGENTS.md

<!-- BEGIN maintaining-agent-docs (generated) -->
## Purpose & Mission

Develop this repository as an evidence-first Claude Agent SDK portfolio project demonstrating real application-level use of the Claude Agent SDK through stateless queries, interactive sessions, custom tools/MCP, async control flow, and a typed FastAPI boundary. Prefer small, inspectable, testable changes over feature breadth.

## Setup & Installation

- Prerequisites: Python `>=3.11` ([pyproject.toml:6](pyproject.toml)), `uv` package manager ([pyproject.toml](pyproject.toml), [Makefile:4](Makefile))
- Install dependencies: `uv sync --all-groups` or `make setup` ([Makefile:3-4](Makefile), [.github/workflows/ci.yml:28](.github/workflows/ci.yml))
- Environment config: `cp .env.example .env` ([README.md:140](README.md))
- Lock dependencies: `uv lock` or `make lock` ([Makefile:6-7](Makefile))

## Build, Run & Examples

- Simple stateless query: `uv run python examples/01_simple_query.py` or `make simple` ([Makefile:9-10](Makefile))
- Interactive terminal CLI: `uv run python examples/02_terminal_cli.py` or `make cli` ([Makefile:12-13](Makefile))
- FastAPI compatibility server: `uv run python examples/03_api_server.py` or `make api` ([Makefile:21-22](Makefile))
- Custom MCP tool: `uv run python examples/04_tool_use.py` or `make tool` ([Makefile:15-16](Makefile))
- PreToolUse permission hook: `uv run python examples/05_permission_hook.py` or `make hook` ([Makefile:18-19](Makefile))

## Test & Verification (Definition of Done)

Before a PR or task is considered complete:

```bash
make verify
```

Equivalent sub-commands:
- Linting & formatting check: `uv run ruff check .` && `uv run ruff format --check .` ([Makefile:28-29](Makefile))
- Format fixes: `uv run ruff check --fix .` && `uv run ruff format .` ([Makefile:32-33](Makefile))
- Typecheck: `uv run mypy src examples tests` ([Makefile:36](Makefile))
- Unit / integration tests (offline): `uv run pytest` ([Makefile:25](Makefile)) or `uv run pytest -m "not live"` ([.github/workflows/ci.yml:39](.github/workflows/ci.yml))
- Optional live smoke tests: `RUN_LIVE_CLAUDE_TESTS=1 uv run pytest -m live tests/live/test_sdk_smoke.py` ([README.md:179-180](README.md))

## Code Style & Architecture Conventions

- Python 3.11+ with strict type checking enabled (`mypy` strict mode in [pyproject.toml:45](pyproject.toml)).
- Async-first on Claude Agent SDK boundaries.
- Pydantic models for HTTP contracts and settings ([pyproject.toml:13-14](pyproject.toml)).
- Dependency injection at the FastAPI boundary ([src/claude_agent_lab/api.py](src/claude_agent_lab/api.py)).
- Explicit error mapping ([src/claude_agent_lab/errors.py](src/claude_agent_lab/errors.py)).
- Unit and integration tests must run without live credentials.
- Prefer direct, explicit code over framework-heavy indirection.
- Do not silently accept unsupported OpenAI fields or swallow SDK errors.
- Do not add vector databases or RAG just to make the repo larger.

## Project Structure

- `src/claude_agent_lab/` — core package (API router, SDK adapter, config, error mappings, tools, session store)
- `examples/` — runnable standalone examples (01 query, 02 CLI, 03 API, 04 tool use, 05 permission hook)
- `tests/` — unit, integration (fake SDK), and live smoke test suites
- `docs/` — architectural design, PRD, security posture, roadmap, and evidence mappings

## Safety Boundaries & Non-negotiable Rules

1. Do not claim a feature in README/EVIDENCE until concrete source code and a test or manual verification path exist.
2. Keep `claude-agent-sdk` usage explicit; do not hide all SDK calls behind abstractions.
3. No secrets, API keys, session credentials, or private transcripts in Git.
4. Do not enable Bash, unrestricted filesystem writes, or dangerous permission modes by default.
5. Live Claude calls must remain opt-in in tests.
6. Preserve the distinction between Claude Agent SDK application development and merely using Claude/Codex as coding assistants.
7. Keep the OpenAI compatibility claim limited to the implemented request/response subset.

## High-Risk Paths

- `src/claude_agent_lab/sdk_adapter.py` — core adapter interfacing with Claude Agent SDK lifecycle.
- `src/claude_agent_lab/api.py` & `src/claude_agent_lab/api_models.py` — public HTTP API contract and validation.
- `src/claude_agent_lab/tools/tool_policy.py` — deterministic tool authorization and permission hook.
<!-- END maintaining-agent-docs -->
