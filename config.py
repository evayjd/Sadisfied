DATABASE_URL = "sqlite:///sadisfied.db"
# config.py

from pydantic import BaseSettings
class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
settings = Settings()