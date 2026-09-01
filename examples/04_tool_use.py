#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import sys

from claude_agent_sdk import ClaudeSDKClient, ResultMessage

from claude_agent_lab.config import get_settings
from claude_agent_lab.messages import extract_assistant_text
from claude_agent_lab.sdk_adapter import ClaudeAgentGateway
from claude_agent_lab.tools.project_facts import create_project_facts_server

TOOL_NAME = "mcp__portfolio__get_project_facts"


async def main() -> int:
    settings = get_settings()
    gateway = ClaudeAgentGateway(settings)
    server = create_project_facts_server()
    options = gateway.build_options(
        system_prompt=(
            "You are demonstrating tool use. When asked about this repository, use the "
            "get_project_facts tool before answering."
        ),
        mcp_servers={"portfolio": server},
        allowed_tools=[TOOL_NAME],
    )

    prompt = (
        "Use the project facts tool with topic 'api', then summarize the result in one sentence."
    )

    try:
        async with asyncio.timeout(settings.turn_timeout_seconds):
            async with ClaudeSDKClient(options=options) as client:
                await client.query(prompt)
                async for message in client.receive_response():
                    text = extract_assistant_text(message)
                    if text:
                        print(text, end="")
                    if isinstance(message, ResultMessage) and message.is_error:
                        print(message.result or "SDK error", file=sys.stderr)
                        return 1
    except TimeoutError:
        print("error: tool-use demo timed out", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
