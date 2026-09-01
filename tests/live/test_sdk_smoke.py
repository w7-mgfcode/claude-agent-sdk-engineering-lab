from __future__ import annotations

import os

import pytest

from claude_agent_lab.config import Settings
from claude_agent_lab.sdk_adapter import ClaudeAgentGateway

pytestmark = pytest.mark.live


@pytest.mark.asyncio
async def test_live_one_shot_sdk_smoke() -> None:
    if os.getenv("RUN_LIVE_CLAUDE_TESTS") != "1":
        pytest.skip("set RUN_LIVE_CLAUDE_TESTS=1 to make a live Claude Agent SDK call")

    gateway = ClaudeAgentGateway(Settings(max_turns=1, max_budget_usd=0.05))
    result = await gateway.complete("Reply with exactly: SDK_SMOKE_OK")

    assert result.text.strip()
