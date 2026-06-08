import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Theme(str, enum.Enum):
    light = "light"
    dark = "dark"


class DigestFrequency(str, enum.Enum):
    realtime = "realtime"
    daily = "daily"
    weekly = "weekly"
    never = "never"


class UserPreference(Base, TimestampMixin):
    """User preference model for theme, language, notifications, timezone."""
    __tablename__ = "user_preferences"
    __table_args__ = (
        {"schema": None},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    theme: Mapped[Theme] = mapped_column(
        Enum(Theme), default=Theme.light, nullable=False
    )
    language: Mapped[str] = mapped_column(String(10), default="en")
    email_notifications: Mapped[dict] = mapped_column(JSON, default=dict)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    digest_frequency: Mapped[DigestFrequency] = mapped_column(
        Enum(DigestFrequency), default=DigestFrequency.daily, nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="preferences")
