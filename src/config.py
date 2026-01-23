"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "sqlite:///data/greenai.db"

    # Application
    secret_key: str = "dev-secret-key-change-in-production"
    debug: bool = True
    log_level: str = "INFO"
    
    # Scheduling
    collection_hour: int = 6
    timezone: str = "UTC"
    
    # Data Sources (optional API keys)
    arxiv_api_key: Optional[str] = None
    serp_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()
