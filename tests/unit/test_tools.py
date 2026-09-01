import pytest

from claude_agent_lab.tools.project_facts import get_project_fact, get_project_facts_tool


def test_known_project_fact() -> None:
    assert "FastAPI" in get_project_fact("api")


def test_unknown_project_fact_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown topic"):
        get_project_fact("production-scale")


@pytest.mark.asyncio
async def test_get_project_facts_tool_success() -> None:
    result = await get_project_facts_tool.handler({"topic": "api"})
    assert result["is_error"] is False
    assert "FastAPI" in result["content"][0]["text"]


@pytest.mark.asyncio
async def test_get_project_facts_tool_invalid_topic() -> None:
    result = await get_project_facts_tool.handler({"topic": "invalid_topic"})
    assert result["is_error"] is True
    assert "Unknown topic" in result["content"][0]["text"]


@pytest.mark.asyncio
async def test_get_project_facts_tool_missing_arg() -> None:
    result = await get_project_facts_tool.handler({})
    assert result["is_error"] is True
    assert "Unknown topic" in result["content"][0]["text"]
