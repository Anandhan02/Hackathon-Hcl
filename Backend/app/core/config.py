from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "SmartBank"
    SECRET_KEY: str = Field(..., description="JWT secret key")
    MONGO_URI: str = Field(..., description="MongoDB URI")
    MONGO_DB: str = "smartbank"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance"""
    return Settings()

settings = get_settings()
