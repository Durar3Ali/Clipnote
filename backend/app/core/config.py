"""Configuration management using environment variables."""

from functools import lru_cache
from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # CORS configuration
    allowed_origins: str = Field(
        default="http://localhost:5173",
        description="Comma-separated list of allowed CORS origins"
    )
    
    # Text length constraints
    min_text_length: int = Field(
        default=100,
        description="Minimum text length in characters for summarization"
    )
    max_text_length: int = Field(
        default=50000,
        description="Maximum text length in characters to prevent abuse"
    )
    
    # Default summarization mode
    default_summary_mode: Literal["brief", "standard", "detailed"] = Field(
        default="standard",
        description="Default summarization mode"
    )
    
    # API configuration
    api_title: str = Field(default="Clipnote API", description="API title")
    api_version: str = Field(default="2.0.0", description="API version")

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
