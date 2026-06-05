from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import User
from app.core.security import pwd_context, create_access_token, create_refresh_token
from app.schemas import UserCreate, UserResponse


class UserService:
    """User business logic service."""

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create new user with hashed password."""
        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            phone_encrypted=user_data.phone,
        )
        db.add(user)
        await db.flush()
        return user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        """Retrieve user by email."""
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
        """Retrieve user by ID."""
        return await db.get(User, user_id)

    @staticmethod
    async def verify_password(user: User, password: str) -> bool:
        """Verify user password."""
        return pwd_context.verify(password, user.hashed_password)
