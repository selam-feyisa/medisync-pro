import uuid
import enum
from sqlalchemy import String, Boolean, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    admin = 'admin'
    doctor = 'doctor'
    nurse = 'nurse'
    receptionist = 'receptionist'
    patient = 'patient'


class AuthProvider(str, enum.Enum):
    local = 'local'
    google = 'google'


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    phone_encrypted: Mapped[str | None] = mapped_column(Text)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.patient,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_secret: Mapped[str | None] = mapped_column(String(64))

    auth_provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider),
        default=AuthProvider.local,
        nullable=False
    )