# Movement 03 — Subprocess Resilience & Fault-Injection Suite

## Objective

Harden the SDK adapter and API boundaries against edge-case failures, hanging subprocesses, tool runtime exceptions, policy rejections, and malformed inputs.

---

## Failure Scenarios & Mitigation Strategies

```mermaid
graph TD
    A[Failure Scenarios] --> B[Turn Timeout Exceeded]
    A --> C[MCP Tool Exception]
    A --> D[PreToolUse Policy Deny]
    A --> E[Client Payload Violations]

    B --> B1[Wrap in asyncio.timeout -> GatewayTimeoutError (HTTP 504)]
    C --> C1[Catch in MCP boundary -> Return formatted ToolResult isError=True]
    D --> D1[Return HookResponse(deny) -> Inform model without process abort]
    E --> E1[Pydantic strict validation -> Fast HTTP 422 with exact field error]
```

---

## Implementation Tasks

### 1. Dedicated Resilience Test Module
- Create `tests/unit/test_resilience.py`:
  - **Timeout Test**: Simulate hanging SDK stream; verify `asyncio.TimeoutError` maps cleanly to `GatewayTimeoutError` with appropriate HTTP 504 status.
  - **Tool Failure Test**: Test behavior when an MCP tool raises unhandled runtime exceptions. Verify error feedback payload structure.
  - **Hook Rejection Test**: Simulate `PreToolUse` hook denial; ensure the model receives structured policy denial message and can formulate a graceful fallback response.
  - **Malformed Payload Test**: Test request bodies with invalid types, extra parameters, or negative timeouts.

### 2. Error Mapping Enhancements
- Audit [src/claude_agent_lab/errors.py](../../src/claude_agent_lab/errors.py):
  - Ensure zero raw Python stack traces are exposed in API error payloads.
  - Add standard error payload schemas (`ErrorDetail`, `ErrorResponse`).

### 3. Graceful Shutdown & Context Cleanup
- Verify async context managers cleanly release all child processes and task groups upon receiving `SIGINT`/`SIGTERM`.

---

## Definition of Done

- [ ] `tests/unit/test_resilience.py` provides 100% coverage over timeout, tool failure, and policy denial scenarios.
- [ ] API responses maintain strict OpenAI-compliant error structures without exposing stack traces.
- [ ] `make verify` passes with exit code 0.
