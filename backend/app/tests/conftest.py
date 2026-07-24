import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.core.config import get_settings


@pytest.fixture(scope="function")
async def db_engine():
    """Create test database engine."""
    settings = get_settings()
    # Use in-memory SQLite for tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="function")
async def db(db_engine):
    """Create test database session."""
    from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionClass
    from sqlalchemy.orm import sessionmaker

    async_session = sessionmaker(
        db_engine,
        class_=AsyncSessionClass,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
def test_user_data():
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "phone": None,
    }


@pytest.fixture
def test_workspace_data():
    """Sample workspace data."""
    return {
        "name": "Test Workspace",
        "slug": "test-workspace",
        "description": "A workspace for testing",
    }


@pytest.fixture
def test_project_data():
    """Sample project data."""
    return {
        "name": "Test Project",
        "slug": "test-project",
        "description": "A project for testing",
        "visibility": "private",
    }


@pytest.fixture
async def client(db) -> "AsyncGenerator[AsyncClient, None]":
    """Create a test client with database dependency override."""
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    from app.core.database import get_db

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
