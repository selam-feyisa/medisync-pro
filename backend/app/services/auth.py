from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import uuid

from app.core.security import create_access_token, create_refresh_token
from app.models import User
from app.services.user import UserService


class AuthService:
    """Authentication business logic service."""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.access_token_expire_minutes = 15
        self.refresh_token_expire_days = 7

    async def authenticate_user(
        self, db: AsyncSession, email: str, password: str
    ) -> User | None:
        """Authenticate user with email and password."""
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not await UserService.verify_password(user, password):
            return None
        return user

    async def create_tokens(self, user_id: uuid.UUID) -> dict:
        """Create access and refresh tokens."""
        access_token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=self.access_token_expire_minutes),
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=self.refresh_token_expire_days),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
        }

    async def blacklist_token(self, token: str, expires_in_seconds: int) -> None:
        """Blacklist refresh token on logout."""
        await self.redis.setex(f"blacklist:{token}", expires_in_seconds, "1")

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return bool(await self.redis.get(f"blacklist:{token}"))
