from claude_agent_lab.tools.tool_policy import evaluate_tool_use

ALLOWED = frozenset({"mcp__portfolio__get_project_facts"})


def test_allowed_tool_is_allowed() -> None:
    decision = evaluate_tool_use("mcp__portfolio__get_project_facts", ALLOWED)
    assert decision.allow is True
    assert "allowed-tools policy" in decision.reason


def test_unlisted_tool_is_denied() -> None:
    decision = evaluate_tool_use("Bash", ALLOWED)
    assert decision.allow is False
    assert "not in the allowed-tools policy" in decision.reason
