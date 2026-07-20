import re
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, ""


def validate_slug(slug: str) -> bool:
    """Validate project slug format."""
    pattern = r'^[a-z0-9-]+$'
    return re.match(pattern, slug) is not None


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input."""
    if not value:
        return value
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Truncate if too long
    if len(value) > max_length:
        value = value[:max_length]
    
    return value


class ValidationMixin:
    """Mixin for common validation methods."""
    
    @validator('email')
    def validate_email_field(cls, v):
        if v and not validate_email(v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('slug')
    def validate_slug_field(cls, v):
        if v and not validate_slug(v):
            raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


def validate_pagination(page: int = 1, limit: int = 20) -> tuple[int, int]:
    """Validate pagination parameters."""
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    return page, limit


def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format."""
    import uuid
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False
