# Security and Permission Model

This is an agent-capable SDK demo, so safe defaults are part of the engineering evidence.

## Hard rules

1. Credentials are never committed. `.env` is ignored.
2. The demo does not use `bypassPermissions`.
3. Bash is not enabled by default.
4. Unrestricted filesystem write access is not enabled by default.
5. The custom tool is deterministic and read-only.
6. Live tests are opt-in.
7. API responses map internal failures to stable error bodies rather than returning raw tracebacks.
8. Prompt content is not logged by default.

## Tool permissions

`examples/04_tool_use.py` registers exactly one MCP tool and puts exactly that tool in `allowed_tools`. This is deliberate: agent demos should show a least-privilege mental model, not merely maximum capability.

## Expanding the tool surface

Before adding Read/Write/Bash/network tools:

- document why the capability is needed;
- add a narrow permission policy;
- add a negative test or hook where practical;
- update `docs/EVIDENCE.md` only after the implementation exists;
- do not expose a dangerous tool through the HTTP example by default.
