from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentResult:
    text: str
    session_id: str | None = None
    total_cost_usd: float | None = None
    num_turns: int | None = None
