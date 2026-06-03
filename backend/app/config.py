"""アプリケーション設定"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AI面接トレーナー"
    debug: bool = True

    # Database（SQLite 開発 / PostgreSQL 本番）
    database_url: str = ""
    
    @property
    def effective_db_url(self) -> str:
        url = self.database_url
        if not url:
            import os
            url = os.environ.get("DATABASE_URL", "sqlite:///./data/interview_trainer.db")
        return url.replace("postgres://", "postgresql://")

    # LLM API
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-4-20250514"

    # JWT
    jwt_secret: str = "development-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 72

    # CORS（* = allow all origins）
    cors_origins: str = "*"

    @property
    def cors_origin_list(self) -> list[str]:
        src = self.cors_origins or "*"
        if src.strip() == "*":
            return ["*"]
        return [o.strip() for o in src.split(",")]

    # STT
    whisper_model_size: str = "base"

    # TTS
    voicevox_url: str = "http://localhost:50021"
    voicevox_speaker: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
