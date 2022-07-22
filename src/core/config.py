import secrets
from typing import Union
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str

    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    CORS_ORIGINS: list

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
