from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from backend.app.schemas.user import UserResponse
from backend.app.core.security import get_current_user
from backend.app.core.database import get_db
from backend.app.models.user import User

router = APIRouter(prefix="/users", tags=["Profile"])


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    timezone: Optional[str] = None


@router.get("/me")
async def get_my_profile(user=Depends(get_current_user)):
    return user


@router.patch("/me")
async def update_profile(
    request: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile."""
    if request.full_name:
        user.full_name = request.full_name
    if request.timezone:
        user.timezone = request.timezone
    await db.commit()
    await db.refresh(user)
    return user