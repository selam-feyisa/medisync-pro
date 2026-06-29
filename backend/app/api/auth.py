from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import redis.asyncio as aioredis
from backend.app.core.database import get_db
from backend.app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token
)
from backend.app.models.user import User, UserRole
from app.core.config import settings

router = APIRouter(prefix="/auth")

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.patient

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

@router.post('/register', status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(409, detail='Email already registered')
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'id': str(user.id), 'email': user.email, 'message': 'Registration successful'}

@router.post('/login', response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail='Invalid email or password')
    if not user.is_active:
        raise HTTPException(403, detail='Account is disabled')
    access_token = create_access_token(str(user.id), user.role.value)
    refresh_token, jti = create_refresh_token(str(user.id))
    r = aioredis.from_url(settings.REDIS_URL)
    await r.setex(
        f'refresh:{user.id}:{jti}',
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        '1'
    )
    await r.aclose()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)