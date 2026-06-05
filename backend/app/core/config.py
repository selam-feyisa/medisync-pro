from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = 'redis://localhost:6379'
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str
    MINIO_URL: str = 'http://localhost:9000'
    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'

    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
