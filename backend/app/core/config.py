from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///./medisync.db'
    REDIS_URL: str = 'redis://localhost:6379'
    SECRET_KEY: str = 'development-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = 'development-encryption-key'
    MINIO_URL: str = 'localhost:9000'
    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'
    MINIO_BUCKET_NAME: str = 'medisync'
    FRONTEND_URL: str = 'http://localhost:3000'
    # Optional SMTP settings for sending verification and reset emails
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_TLS: bool = False
    SMTP_FROM: str | None = None

    model_config = ConfigDict(
        env_file='.env',
        extra='ignore'
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

