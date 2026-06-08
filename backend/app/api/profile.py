from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from backend.app.schemas.user import UserResponse
from backend.app.core.security import get_current_user, verify_password, hash_password
from backend.app.core.database import get_db
from backend.app.models.user import User

router = APIRouter(prefix="/users", tags=["Profile"])


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    timezone: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


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


@router.patch("/me/password")
async def change_password(
    request: PasswordChange,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change user password with old password verification."""
    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    user.hashed_password = hash_password(request.new_password)
    await db.commit()
    return {"message": "Password changed successfully"}