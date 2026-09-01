# Engineering Evidence Map

This file maps portfolio claims to inspectable source code. The rule is simple: **a README sentence is not evidence by itself**.

| Claim | Exact evidence | What it demonstrates |
|---|---|---|
| Claude Agent SDK one-shot execution | `src/claude_agent_lab/sdk_adapter.py::ClaudeAgentGateway.complete` and `examples/01_simple_query.py` | real `query()` use, async iterator consumption, result/error handling |
| Stateful Claude Agent SDK client | `examples/02_terminal_cli.py::interactive_session` | `ClaudeSDKClient`, async context lifecycle, multi-turn query/receive flow |
| Session resume | `examples/02_terminal_cli.py` + `src/claude_agent_lab/session_store.py` | SDK `resume` option plus non-secret local convenience metadata |
| Async Python | `sdk_adapter.py::complete`, `02_terminal_cli.py::run_turn`, `04_tool_use.py` | `asyncio.timeout`, async iterators, async context managers, interruption path |
| Custom Agent SDK tool | `src/claude_agent_lab/tools/project_facts.py` | `@tool`, in-process `create_sdk_mcp_server`, input validation |
| Tool execution through ClaudeSDKClient | `examples/04_tool_use.py` | MCP registration, narrow `allowed_tools`, client execution |
| FastAPI integration | `src/claude_agent_lab/api.py` | typed HTTP boundary, DI, middleware, stable error mapping |
| OpenAI-shaped API subset | `src/claude_agent_lab/api_models.py` + API tests | explicit supported contract; unsupported fields rejected |
| Credential-free verification | `tests/integration/test_api_fake_sdk.py` | API behavior tested through a fake gateway without paid/live call |
| Live SDK smoke path | `tests/live/test_sdk_smoke.py` | opt-in real Agent SDK invocation |
| Security-aware defaults | `docs/SECURITY.md`, `examples/04_tool_use.py` | no Bash/unrestricted write/bypassPermissions default |
| Deterministic PreToolUse permission hook | `src/claude_agent_lab/tools/tool_policy.py` + `examples/05_permission_hook.py` + `tests/unit/test_tool_policy.py` | Agent SDK `ClaudeAgentOptions.hooks`/`HookMatcher` API; policy logic tested independently of any live SDK call |

## Safe portfolio claim after live verification

Once the live examples have been run successfully on the pinned SDK version, this repo is designed to support the following statement:

> I built Python examples with the Claude Agent SDK covering stateless `query()` execution, stateful `ClaudeSDKClient` sessions, a custom SDK MCP tool, async timeout/lifecycle handling, and a typed FastAPI integration.

## Do not claim from this repository

- enterprise production operation;
- high availability or distributed sessions;
- full OpenAI API compatibility;
- LangGraph or OpenAI Codex SDK application integration;
- Milvus, Qdrant, or Weaviate experience;
- production security certification.
