from __future__ import annotations

from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

PROJECT_FACTS: dict[str, str] = {
    "simple-query": "Example 01 uses claude_agent_sdk.query() and consumes its async message iterator.",
    "stateful-client": "Example 02 uses ClaudeSDKClient for a multi-turn interactive session.",
    "api": "The FastAPI example exposes a typed /v1/chat/completions compatibility subset.",
    "async": "The project uses async iterators, async context managers, asyncio.timeout and interruption-aware control flow.",
    "testing": "Unit and fake-gateway integration tests run without live Claude credentials; the live smoke test is opt-in.",
    "security": "The default examples do not enable Bash, unrestricted filesystem writes, or bypassPermissions.",
}


def get_project_fact(topic: str) -> str:
    key = topic.strip().lower()
    if key not in PROJECT_FACTS:
        valid = ", ".join(sorted(PROJECT_FACTS))
        raise ValueError(f"Unknown topic '{topic}'. Valid topics: {valid}")
    return PROJECT_FACTS[key]


@tool(
    "get_project_facts",
    "Return a deterministic fact about this Claude Agent SDK engineering repository.",
    {"topic": str},
)
async def get_project_facts_tool(args: dict[str, Any]) -> dict[str, Any]:
    topic = str(args.get("topic", ""))
    try:
        fact = get_project_fact(topic)
    except ValueError as exc:
        return {
            "content": [{"type": "text", "text": str(exc)}],
            "is_error": True,
        }

    return {
        "content": [{"type": "text", "text": fact}],
        "is_error": False,
    }


def create_project_facts_server() -> Any:
    """Create an in-process SDK MCP server containing one harmless read-only tool."""
    return create_sdk_mcp_server(
        name="portfolio",
        tools=[get_project_facts_tool],
    )
