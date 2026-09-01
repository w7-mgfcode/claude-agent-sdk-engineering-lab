# Troubleshooting

## SDK authentication / transport failure

The Claude Agent SDK uses the Claude Code runtime/CLI integration. Authentication is environment-specific and intentionally not embedded in this repository. Confirm your local Claude Agent SDK / Claude Code authentication first, then rerun `examples/01_simple_query.py`.

## Session resume starts differently than expected

Resume behavior is owned by the SDK and can depend on its local session store and working directory. This demo stores the previous `session_id` and `cwd` only; it does not reimplement the SDK transcript store.

Use an explicit ID:

```bash
uv run python examples/02_terminal_cli.py --resume <session-id>
```

## MCP/tool demo fails after dependency upgrades

The pinned Agent SDK currently constrains its MCP dependency to the v1 line. Do not force MCP v2 into the same environment without first checking upstream Agent SDK support. Regenerate the lockfile only after deliberate compatibility testing.

## CI passes but live test fails

That is possible by design. Default CI verifies local logic through fake boundaries and does not require credentials. Run the opt-in live test to validate your local SDK/auth environment.
