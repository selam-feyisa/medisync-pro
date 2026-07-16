import uuid
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class NotificationPreference(Base, TimestampMixin):
    """NotificationPreference model - user notification settings."""
    __tablename__ = "notification_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    ticket_assigned: Mapped[bool] = mapped_column(Boolean, default=True)
    ticket_mentioned: Mapped[bool] = mapped_column(Boolean, default=True)
    ticket_updated: Mapped[bool] = mapped_column(Boolean, default=False)
    ticket_commented: Mapped[bool] = mapped_column(Boolean, default=True)
    sprint_started: Mapped[bool] = mapped_column(Boolean, default=True)
    sprint_completed: Mapped[bool] = mapped_column(Boolean, default=True)
    workspace_invited: Mapped[bool] = mapped_column(Boolean, default=True)
    digest_frequency: Mapped[str] = mapped_column(String(20), default="daily")  # instant, daily, weekly

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notification_preferences")
