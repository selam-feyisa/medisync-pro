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
from backend.app.core.email_utils import send_email, build_verification_link, build_reset_link
from datetime import datetime, timedelta
import secrets

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
    # create email verification token and send email (stored temporarily in reset_token)
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(hours=48)
    await db.commit()
    verification_link = build_verification_link(token)
    await send_email(user.email, 'Verify your email', f'Please verify your email by visiting: {verification_link}')
    return {'id': str(user.id), 'email': user.email, 'message': 'Registration successful'}


class VerifyEmailRequest(BaseModel):
    token: str


@router.post('/verify-email')
async def verify_email(request: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.reset_token == request.token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail='Invalid token')
    if user.reset_token_expires_at and user.reset_token_expires_at < datetime.utcnow():
        raise HTTPException(400, detail='Token expired')
    user.email_verified = True
    user.reset_token = None
    user.reset_token_expires_at = None
    await db.commit()
    return {'message': 'Email verified'}


class PasswordResetRequest(BaseModel):
    email: str


@router.post('/password-reset')
async def password_reset_request(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        # do not reveal existence
        return {'message': 'If an account exists, a reset email was sent'}
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(hours=2)
    await db.commit()
    reset_link = build_reset_link(token)
    await send_email(user.email, 'Reset your password', f'Reset link: {reset_link}')
    return {'message': 'If an account exists, a reset email was sent'}


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


@router.post('/password-reset/confirm')
async def password_reset_confirm(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.reset_token == data.token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail='Invalid token')
    if user.reset_token_expires_at and user.reset_token_expires_at < datetime.utcnow():
        raise HTTPException(400, detail='Token expired')
    user.hashed_password = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    await db.commit()
    return {'message': 'Password has been reset'}

@router.post('/login', response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail='Invalid email or password')
    if not user.is_active:
        raise HTTPException(403, detail='Account is disabled')
    if not user.email_verified:
        raise HTTPException(403, detail='Email address not verified')
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