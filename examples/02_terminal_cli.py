#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import contextlib
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeSDKClient, ResultMessage

from claude_agent_lab.config import get_settings
from claude_agent_lab.logging_utils import configure_logging
from claude_agent_lab.messages import extract_assistant_text
from claude_agent_lab.sdk_adapter import ClaudeAgentGateway
from claude_agent_lab.session_store import LocalSessionStore, SessionMetadata


async def run_turn(client: ClaudeSDKClient, prompt: str, timeout_seconds: float) -> str | None:
    """Send one user turn and consume the SDK response stream."""
    session_id: str | None = None
    printed_any = False

    try:
        async with asyncio.timeout(timeout_seconds):
            await client.query(prompt)
            async for message in client.receive_response():
                text = extract_assistant_text(message)
                if text:
                    print(text, end="", flush=True)
                    printed_any = True
                if isinstance(message, ResultMessage):
                    session_id = message.session_id
                    if message.is_error:
                        raise RuntimeError(message.result or "Claude Agent SDK returned an error")
    except TimeoutError:
        with contextlib.suppress(Exception):
            await client.interrupt()
        raise

    if printed_any:
        print()
    return session_id


async def interactive_session(resume: str | None, store: LocalSessionStore) -> str:
    settings = get_settings()
    gateway = ClaudeAgentGateway(settings)
    options = gateway.build_options(resume=resume)

    print("Claude Agent SDK terminal demo")
    print("Commands: /help /session /new /exit")
    if resume:
        print(f"Resuming SDK session: {resume}")

    current_session_id = resume

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                user_input = await asyncio.to_thread(input, "you> ")
            except EOFError:
                return "exit"

            prompt = user_input.strip()
            if not prompt:
                continue
            if prompt == "/exit":
                return "exit"
            if prompt == "/help":
                print("/session shows the active ID; /new restarts the SDK client; /exit quits.")
                continue
            if prompt == "/session":
                print(current_session_id or "No ResultMessage session ID received yet.")
                continue
            if prompt == "/new":
                store.clear()
                return "new"

            try:
                new_session_id = await run_turn(
                    client,
                    prompt,
                    timeout_seconds=settings.turn_timeout_seconds,
                )
            except TimeoutError:
                print(
                    "error: turn timed out; restarting the SDK session is recommended",
                    file=sys.stderr,
                )
                continue
            except Exception as exc:
                print(f"error: {exc}", file=sys.stderr)
                continue

            if new_session_id:
                current_session_id = new_session_id
                store.save(SessionMetadata(session_id=new_session_id, cwd=str(Path.cwd())))

    return "exit"


async def main() -> int:
    parser = argparse.ArgumentParser(description="Interactive ClaudeSDKClient example")
    parser.add_argument(
        "--resume",
        metavar="SESSION_ID|last",
        default=None,
        help="Resume an explicit SDK session ID, or the last locally stored ID",
    )
    args = parser.parse_args()

    settings = get_settings()
    configure_logging(settings.log_level)
    store = LocalSessionStore(settings.state_dir / "session.json")

    resume: str | None = args.resume
    if resume == "last":
        metadata = store.load()
        if metadata is None:
            print("error: no local session metadata found", file=sys.stderr)
            return 2
        if metadata.cwd != str(Path.cwd()):
            print(
                f"warning: stored session cwd was {metadata.cwd!r}; current cwd is {str(Path.cwd())!r}",
                file=sys.stderr,
            )
        resume = metadata.session_id

    try:
        while True:
            action = await interactive_session(resume, store)
            if action == "exit":
                return 0
            resume = None
    except KeyboardInterrupt:
        print("\nbye")
        return 130


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
