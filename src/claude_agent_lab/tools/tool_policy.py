from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from claude_agent_sdk import HookCallback, HookContext, HookInput, HookJSONOutput
from claude_agent_sdk.types import PreToolUseHookInput


@dataclass(frozen=True, slots=True)
class ToolPolicyDecision:
    """Deterministic outcome of evaluating one tool-use request."""

    allow: bool
    reason: str


def evaluate_tool_use(tool_name: str, allowed_tools: frozenset[str]) -> ToolPolicyDecision:
    """Allow only tools present in `allowed_tools`; deny everything else with a stated reason."""
    if tool_name in allowed_tools:
        return ToolPolicyDecision(
            allow=True, reason=f"'{tool_name}' is in the allowed-tools policy"
        )
    return ToolPolicyDecision(
        allow=False, reason=f"'{tool_name}' is not in the allowed-tools policy"
    )


def build_pre_tool_use_hook(allowed_tools: frozenset[str]) -> HookCallback:
    """Adapt `evaluate_tool_use` into a Claude Agent SDK PreToolUse hook callback."""

    async def pre_tool_use_hook(
        input_data: HookInput,
        tool_use_id: str | None,
        context: HookContext,
    ) -> HookJSONOutput:
        pre_tool_input = cast(PreToolUseHookInput, input_data)
        tool_name = pre_tool_input["tool_name"]
        decision = evaluate_tool_use(tool_name, allowed_tools)
        permission_decision: Literal["allow", "deny"] = "allow" if decision.allow else "deny"
        print(f"policy: tool={tool_name} decision={permission_decision} reason={decision.reason}")
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": permission_decision,
                "permissionDecisionReason": decision.reason,
            }
        }

    return pre_tool_use_hook
