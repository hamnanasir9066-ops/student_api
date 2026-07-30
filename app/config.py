import os
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings
    SettingsConfigDict = None


class Settings(BaseSettings):
    """
    Centralized Application Configuration.
    Loads settings from environment variables or a .env file securely.
    """
    SECRET_KEY: str = "secret-key-change-in-production-environment-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "12345"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str = "fastapi_db"

    if SettingsConfigDict:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )
    else:
        class Config:
            env_file = ".env"


settings = Settings()
