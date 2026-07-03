from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from backend.app.schemas.user import UserResponse
from backend.app.core.security import get_current_user, verify_password, hash_password
from backend.app.core.database import get_db
from backend.app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter(prefix="/users", tags=["Profile"])


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    timezone: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@router.get("/me")
async def get_my_profile(db: AsyncSession = Depends(get_db), token_user=Depends(get_current_user)):
    # token_user contains id from JWT payload
    result = await db.execute(select(User).where(User.id == token_user["id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
    if not user.email_verified:
        raise HTTPException(403, detail="Email not verified")
    return user


@router.patch("/me")
async def update_profile(
    request: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    token_user=Depends(get_current_user),
):
    """Update current user profile."""
    result = await db.execute(select(User).where(User.id == token_user["id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
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
    db: AsyncSession = Depends(get_db),
    token_user=Depends(get_current_user),
):
    """Change user password with old password verification."""
    result = await db.execute(select(User).where(User.id == token_user["id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    user.hashed_password = hash_password(request.new_password)
    await db.commit()
    return {"message": "Password changed successfully"}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    db: AsyncSession = Depends(get_db),
    token_user=Depends(get_current_user),
):
    """Soft-delete user account."""
    result = await db.execute(select(User).where(User.id == token_user["id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
    user.is_deleted = True
    await db.commit()


@router.get("/me/preferences")
async def get_preferences(
    db: AsyncSession = Depends(get_db),
    token_user=Depends(get_current_user),
):
    """Get user preferences."""
    from backend.app.models.user_preference import UserPreference
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == token_user["id"])
    )
    preferences = result.scalar_one_or_none()
    if not preferences:
        preferences = UserPreference(user_id=token_user["id"])
        db.add(preferences)
        await db.commit()
        await db.refresh(preferences)
    return preferences


class PreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    digest_frequency: Optional[str] = None


@router.patch("/me/preferences")
async def update_preferences(
    request: PreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    token_user=Depends(get_current_user),
):
    """Update user preferences."""
    from backend.app.models.user_preference import UserPreference
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == token_user["id"])
    )
    preferences = result.scalar_one_or_none()
    if not preferences:
        preferences = UserPreference(user_id=token_user["id"])
        db.add(preferences)
    
    if request.theme:
        preferences.theme = request.theme
    if request.language:
        preferences.language = request.language
    if request.timezone:
        preferences.timezone = request.timezone
    if request.digest_frequency:
        preferences.digest_frequency = request.digest_frequency
    
    await db.commit()
    await db.refresh(preferences)
    return preferences