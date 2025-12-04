import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/auto")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    share_secret_key: str = os.getenv("SHARE_SECRET_KEY", "change-me-in-production")


@lru_cache
def get_settings() -> Settings:
    return Settings()

