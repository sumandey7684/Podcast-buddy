from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = Field(default="Podcast Buddy API")
    version: str = Field(default="0.1.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    default_news_provider: str = Field(default="gnews")
    audio_base_url: str = Field(default="/static/audio")
    gemini_model: str = Field(default="gemini-2.5-flash")
    gemini_max_retries: int = Field(default=3, ge=1, le=5)
    gemini_retry_base_delay_seconds: float = Field(default=1.0, gt=0)
    edge_tts_voice_a: str = Field(default="en-US-AndrewNeural")
    edge_tts_voice_b: str = Field(default="en-US-EmmaNeural")
    news_api_key: str | None = None
    gnews_api_key: str | None = None
    gemini_api_key: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()