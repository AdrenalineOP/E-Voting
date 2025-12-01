from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings and configuration
    """
    # App Info
    APP_NAME: str = "E-Voting System"
    APP_VERSION: str = "7.01"
    APP_DESCRIPTION: str = "Backend API for E-Voting Desktop Application"

    # API Settings
    API_PREFIX: str = "/api"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database Settings (SQLite)
    DATABASE_URL: str = "sqlite:///./evoting.db"
    DATABASE_ECHO: bool = False  # Set to True for SQL query logging

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = True

    # Email/SMTP Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: str = "E-Voting System"

    # OTP Settings
    OTP_LENGTH: int = 5
    OTP_EXPIRY_MINUTES: int = 10

    # Security (for future authentication)
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]  # For Flet desktop app

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Create settings instance
settings = Settings()
