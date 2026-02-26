DATABASE_URL = "sqlite:///sadisfied.db"


from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
settings = Settings()

SUMMARY_TRIGGER = 12
KEEP_LAST_MESSAGES = 6
MAX_HISTORY = 20