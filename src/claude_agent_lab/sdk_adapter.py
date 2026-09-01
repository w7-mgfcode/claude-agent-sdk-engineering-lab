from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
    query,
)
from claude_agent_sdk.types import HookEvent

from claude_agent_lab.config import Settings
from claude_agent_lab.errors import AgentTimeoutError, AgentUpstreamError
from claude_agent_lab.messages import extract_assistant_text, extract_result_text
from claude_agent_lab.models import AgentResult

logger = logging.getLogger(__name__)


class ClaudeAgentGateway:
    """Thin adapter for stateless Claude Agent SDK execution.

    The adapter intentionally exposes SDK concepts rather than hiding them behind a
    framework-agnostic abstraction. That keeps this repository useful as evidence of
    real Claude Agent SDK integration.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def build_options(
        self,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
        resume: str | None = None,
        mcp_servers: dict[str, Any] | None = None,
        allowed_tools: list[str] | None = None,
        hooks: dict[HookEvent, list[HookMatcher]] | None = None,
    ) -> ClaudeAgentOptions:
        return ClaudeAgentOptions(
            model=model or self.settings.claude_model,
            system_prompt=system_prompt,
            max_turns=self.settings.max_turns,
            max_budget_usd=self.settings.max_budget_usd,
            resume=resume,
            cwd=str(Path.cwd()),
            mcp_servers=mcp_servers or {},
            allowed_tools=allowed_tools or [],
            hooks=hooks or {},
        )

    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> AgentResult:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        options = self.build_options(model=model, system_prompt=system_prompt)
        chunks: list[str] = []
        result_message: ResultMessage | None = None

        try:
            async with asyncio.timeout(self.settings.turn_timeout_seconds):
                async for message in query(prompt=prompt, options=options):
                    text = extract_assistant_text(message)
                    if text:
                        chunks.append(text)
                    if isinstance(message, ResultMessage):
                        result_message = message
        except TimeoutError as exc:
            raise AgentTimeoutError(
                f"Claude turn exceeded {self.settings.turn_timeout_seconds:.0f}s timeout"
            ) from exc
        except Exception as exc:
            logger.exception("outcome=error category=sdk_transport")
            raise AgentUpstreamError(str(exc)) from exc

        if result_message is not None and result_message.is_error:
            raise AgentUpstreamError(result_message.result or "Claude Agent SDK returned an error")

        text = "".join(chunks).strip()
        if not text and result_message is not None:
            text = extract_result_text(result_message).strip()

        if not text:
            raise AgentUpstreamError("Claude Agent SDK completed without assistant text")

        return AgentResult(
            text=text,
            session_id=result_message.session_id if result_message else None,
            total_cost_usd=result_message.total_cost_usd if result_message else None,
            num_turns=result_message.num_turns if result_message else None,
        )
