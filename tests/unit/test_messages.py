from claude_agent_sdk import AssistantMessage, TextBlock

from claude_agent_lab.messages import extract_assistant_text


def test_extract_assistant_text_joins_text_blocks() -> None:
    message = AssistantMessage(
        content=[TextBlock(text="hello "), TextBlock(text="world")],
        model="test-model",
    )
    assert extract_assistant_text(message) == "hello world"
