from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import redis.asyncio as aioredis
from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token
)
from app.models.user import User, UserRole, AuthProvider
from app.core.config import settings
from app.core.email_utils import send_email, build_verification_link, build_reset_link
from app.core.oauth import get_google_oauth, get_github_oauth
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


class ResendVerificationRequest(BaseModel):
    email: str


@router.post('/resend-verification')
async def resend_verification(data: ResendVerificationRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        # don't reveal existence
        return {'message': 'If an account exists, a verification email was sent'}
    # simple rate limit: only allow resend every 5 minutes
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    if user.verification_sent_at and (now - user.verification_sent_at) < timedelta(minutes=5):
        raise HTTPException(429, detail='Verification recently sent. Please wait before retrying')
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires_at = now + timedelta(hours=48)
    user.verification_sent_at = now
    await db.commit()
    verification_link = build_verification_link(token)
    await send_email(user.email, 'Verify your email', f'Please verify your email by visiting: {verification_link}')
    return {'message': 'If an account exists, a verification email was sent'}

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
    try:
        r = aioredis.from_url(settings.REDIS_URL)
        await r.setex(
            f'refresh:{user.id}:{jti}',
            settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
            '1'
        )
        await r.aclose()
    except Exception as exc:
        print(f'Warning: Redis unavailable, continuing without refresh token storage: {exc}')
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# OAuth Endpoints

@router.get('/google')
async def google_login(request: Request):
    """Redirect to Google OAuth authorization page."""
    google_oauth = get_google_oauth()
    if not google_oauth:
        raise HTTPException(501, detail='Google OAuth not configured')
    
    redirect_uri = f"{settings.FRONTEND_URL}/auth/google/callback"
    state = secrets.token_urlsafe(32)
    auth_url = google_oauth.get_auth_url(redirect_uri, state)
    
    return {"auth_url": auth_url, "state": state}


@router.get('/google/callback')
async def google_callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    """Handle Google OAuth callback."""
    google_oauth = get_google_oauth()
    if not google_oauth:
        raise HTTPException(501, detail='Google OAuth not configured')
    
    redirect_uri = f"{settings.FRONTEND_URL}/auth/google/callback"
    
    try:
        # Exchange code for token
        token_data = await google_oauth.exchange_code_for_token(code, redirect_uri)
        access_token = token_data.get("access_token")
        
        # Get user info
        user_info = await google_oauth.get_user_info(access_token)
        email = user_info.get("email")
        full_name = user_info.get("name")
        
        if not email:
            raise HTTPException(400, detail='Unable to retrieve email from Google')
        
        # Find or create user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            # Update existing user
            if user.auth_provider != AuthProvider.google:
                user.auth_provider = AuthProvider.google
            if not user.email_verified:
                user.email_verified = True
            if full_name and not user.full_name:
                user.full_name = full_name
        else:
            # Create new user
            user = User(
                email=email,
                full_name=full_name or email.split('@')[0],
                hashed_password=hash_password(secrets.token_urlsafe(32)),  # Random password
                role=UserRole.patient,
                auth_provider=AuthProvider.google,
                email_verified=True,
                is_active=True
            )
            db.add(user)
        
        await db.commit()
        await db.refresh(user)
        
        # Generate tokens
        access_token_jwt = create_access_token(str(user.id), user.role.value)
        refresh_token_jwt, jti = create_refresh_token(str(user.id))
        
        try:
            r = aioredis.from_url(settings.REDIS_URL)
            await r.setex(
                f'refresh:{user.id}:{jti}',
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
                '1'
            )
            await r.aclose()
        except Exception as exc:
            print(f'Warning: Redis unavailable, continuing without refresh token storage: {exc}')
        
        return TokenResponse(access_token=access_token_jwt, refresh_token=refresh_token_jwt)
    
    except Exception as e:
        raise HTTPException(400, detail=f'OAuth authentication failed: {str(e)}')


@router.get('/github')
async def github_login(request: Request):
    """Redirect to GitHub OAuth authorization page."""
    github_oauth = get_github_oauth()
    if not github_oauth:
        raise HTTPException(501, detail='GitHub OAuth not configured')
    
    redirect_uri = f"{settings.FRONTEND_URL}/auth/github/callback"
    state = secrets.token_urlsafe(32)
    auth_url = github_oauth.get_auth_url(redirect_uri, state)
    
    return {"auth_url": auth_url, "state": state}


@router.get('/github/callback')
async def github_callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    """Handle GitHub OAuth callback."""
    github_oauth = get_github_oauth()
    if not github_oauth:
        raise HTTPException(501, detail='GitHub OAuth not configured')
    
    redirect_uri = f"{settings.FRONTEND_URL}/auth/github/callback"
    
    try:
        # Exchange code for token
        token_data = await github_oauth.exchange_code_for_token(code, redirect_uri)
        access_token = token_data.get("access_token")
        
        # Get user info
        user_info = await github_oauth.get_user_info(access_token)
        email = user_info.get("email")
        full_name = user_info.get("name") or user_info.get("login")
        
        if not email:
            raise HTTPException(400, detail='Unable to retrieve email from GitHub (make sure email is public)')
        
        # Find or create user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            # Update existing user
            if user.auth_provider != AuthProvider.github:
                user.auth_provider = AuthProvider.github
            if not user.email_verified:
                user.email_verified = True
            if full_name and not user.full_name:
                user.full_name = full_name
        else:
            # Create new user
            user = User(
                email=email,
                full_name=full_name or email.split('@')[0],
                hashed_password=hash_password(secrets.token_urlsafe(32)),  # Random password
                role=UserRole.patient,
                auth_provider=AuthProvider.github,
                email_verified=True,
                is_active=True
            )
            db.add(user)
        
        await db.commit()
        await db.refresh(user)
        
        # Generate tokens
        access_token_jwt = create_access_token(str(user.id), user.role.value)
        refresh_token_jwt, jti = create_refresh_token(str(user.id))
        
        try:
            r = aioredis.from_url(settings.REDIS_URL)
            await r.setex(
                f'refresh:{user.id}:{jti}',
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
                '1'
            )
            await r.aclose()
        except Exception as exc:
            print(f'Warning: Redis unavailable, continuing without refresh token storage: {exc}')
        
        return TokenResponse(access_token=access_token_jwt, refresh_token=refresh_token_jwt)
    
    except Exception as e:
        raise HTTPException(400, detail=f'OAuth authentication failed: {str(e)}')