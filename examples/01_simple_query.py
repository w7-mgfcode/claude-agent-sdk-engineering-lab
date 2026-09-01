#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import sys

from claude_agent_lab.config import get_settings
from claude_agent_lab.errors import AgentLabError
from claude_agent_lab.logging_utils import configure_logging
from claude_agent_lab.sdk_adapter import ClaudeAgentGateway

DEFAULT_PROMPT = "Explain asyncio.gather vs TaskGroup in three concise bullets."


async def main() -> int:
    parser = argparse.ArgumentParser(description="Stateless Claude Agent SDK query() example")
    parser.add_argument("prompt", nargs="?", default=DEFAULT_PROMPT)
    parser.add_argument("--model", default=None, help="Optional Claude model override")
    args = parser.parse_args()

    settings = get_settings()
    configure_logging(settings.log_level)
    gateway = ClaudeAgentGateway(settings)

    try:
        result = await gateway.complete(args.prompt, model=args.model)
    except (AgentLabError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(result.text)
    if result.session_id:
        print(f"\n[session_id={result.session_id}]", file=sys.stderr)
    if result.total_cost_usd is not None:
        print(f"[cost_usd={result.total_cost_usd:.6f}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
