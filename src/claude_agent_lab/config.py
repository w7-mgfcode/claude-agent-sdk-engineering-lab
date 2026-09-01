from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, environment-backed runtime configuration."""

    model_config = SettingsConfigDict(
        env_prefix="LAB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    claude_model: str | None = None
    turn_timeout_seconds: float = Field(default=90.0, gt=0, le=600)
    max_turns: int = Field(default=4, ge=1, le=20)
    max_budget_usd: float = Field(default=0.25, gt=0, le=10)
    log_level: str = "INFO"

    @field_validator("claude_model", mode="before")
    @classmethod
    def blank_model_means_sdk_default(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def state_dir(self) -> Path:
        return Path(".claude-agent-lab")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
