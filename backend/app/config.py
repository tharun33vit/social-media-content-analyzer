"""Application settings and configuration management."""

import os
from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Social Media Content Analyzer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Gemini LLM Settings
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Upload Settings
    MAX_UPLOAD_SIZE_MB: int = 10

    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    # OCR / Tesseract Settings
    TESSERACT_CMD: Optional[str] = None

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins parsed as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        """Return maximum upload size in bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
