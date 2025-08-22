from __future__ import annotations

from functools import lru_cache
from typing import List, Literal

from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pydantic-settings v2 config
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        env_prefix="APP_",                   # all vars start with APP_
        env_nested_delimiter="__",           # supports nested env names if needed
        extra="ignore",
    )

    # General
    ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False
    APP_NAME: str = "Example API"
    SECRET_KEY: SecretStr

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info"

    # Persistence / integrations
    DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = False
    REDIS_URL: str = "redis://redis-serve:6379/0"

    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] | List[str] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors_csv(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @property
    def uvicorn_options(self) -> dict:
        # Handy bundle for uvicorn.run(...)
        return {
            "host": self.HOST,
            "port": self.PORT,
            "reload": self.DEBUG,
            "log_level": self.LOG_LEVEL,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Importable singleton
settings = get_settings()
