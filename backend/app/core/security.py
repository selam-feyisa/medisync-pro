import uuid
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str, role: str, clinic_id: str = None) -> str:
    """Create JWT access token — expires in ACCESS_TOKEN_EXPIRE_MINUTES."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        'sub': str(user_id),
        'role': role,
        'clinic_id': str(clinic_id) if clinic_id else None,
        'exp': expire,
        'jti': str(uuid.uuid4()),
        'type': 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: str) -> tuple[str, str]:
    """Create refresh token — 7 days. Returns (token, jti).
    Store jti in Redis so we can revoke on logout.
    """
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        'sub': str(user_id),
        'exp': expire,
        'jti': jti,
        'type': 'refresh'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, jti

def decode_token(token: str) -> dict:
    """Decode and verify a JWT. Raises JWTError if invalid or expired."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
