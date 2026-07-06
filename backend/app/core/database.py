from importlib.util import find_spec

from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from app.core.config import settings

# Use SQLite locally when PostgreSQL drivers are unavailable so the app still starts.
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith('postgresql') and find_spec('asyncpg') is None:
    DATABASE_URL = 'sqlite+aiosqlite:///./medisync.db'
    print('Warning: asyncpg is not installed; falling back to sqlite+aiosqlite for local development.')
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """FastAPI dependency — yields DB session, auto-commits or rolls back."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
