from __future__ import annotations

from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from claude_agent_sdk.types import Message


def extract_assistant_text(message: Message) -> str:
    """Extract only visible assistant text from an SDK message."""
    if not isinstance(message, AssistantMessage):
        return ""

    parts = [block.text for block in message.content if isinstance(block, TextBlock)]
    return "".join(parts)


def extract_result_text(message: Message) -> str:
    """Return the SDK's final result text when the message is a ResultMessage."""
    if isinstance(message, ResultMessage) and message.result:
        return message.result
    return ""
