import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.main import app
from app.core.database import get_db

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with TestAsyncSessionLocal() as session:
        async with test_engine.begin() as conn:
            # Create all tables
            from app.models.base import Base
            await conn.run_sync(Base.metadata.create_all)
        
        yield session
        
        # Cleanup
        async with test_engine.begin() as conn:
            from app.models.base import Base
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database dependency override."""
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
