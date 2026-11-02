from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    database_url: str
    redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()
