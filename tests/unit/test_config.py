from claude_agent_lab.config import Settings


def test_blank_model_uses_sdk_default() -> None:
    settings = Settings(claude_model="")
    assert settings.claude_model is None


def test_log_level_is_normalized() -> None:
    settings = Settings(log_level="debug")
    assert settings.log_level == "DEBUG"
