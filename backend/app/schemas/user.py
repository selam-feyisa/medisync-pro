from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None


class UserResponse(UserBase):
    id: uuid.UUID
    phone_encrypted: Optional[str] = None
    mfa_enabled: bool
    auth_provider: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
