# Job-offer fit — what this repository is meant to prove

The target recruiter filter asks for practical evidence around FastAPI/Flask, async Python, a named AI-agent framework, and vector databases.

This repository deliberately targets the **Claude Agent SDK evidence gap** while reinforcing two already-related engineering areas.

| Recruiter signal | Evidence in this repo | Intended interpretation |
|---|---|---|
| FastAPI | `src/claude_agent_lab/api.py` | typed API boundary, DI, validation, middleware, error mapping |
| Async Python | all four runtime examples | meaningful async I/O/control flow, not merely `async def` syntax |
| Claude Agent SDK | `query()`, `ClaudeSDKClient`, SDK MCP tool | direct named-framework application development |
| Vector DB | not implemented here | **do not** use this repo to claim Milvus/Qdrant/Weaviate |

## 5-minute hiring-manager demo

1. Open `examples/01_simple_query.py` and show the one-shot path through `ClaudeAgentGateway.complete`.
2. Open `examples/02_terminal_cli.py` and point out `ClaudeSDKClient`, `client.query`, `receive_response`, timeout and resume.
3. Open `project_facts.py` and `04_tool_use.py` to show `@tool`, `create_sdk_mcp_server`, and the narrow MCP allowlist.
4. Open `api.py` and `test_api_fake_sdk.py` to show FastAPI + testable SDK seam.
5. Run `make verify`, then one live smoke test if credentials are available.

## Interview line

> „A repót direkt úgy építettem, hogy ne csak azt mutassa, hogy Claude API-t hívok. Van benne `query()` és `ClaudeSDKClient` alapú futás, saját in-process MCP tool, async timeout/session lifecycle, illetve egy tesztelhető FastAPI boundary. A live hívások opt-in-ek, a normál CI nem igényel credentialt.”
