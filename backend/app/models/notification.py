import uuid
import enum
from sqlalchemy import String, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class NotificationType(str, enum.Enum):
    ticket_assigned = "ticket_assigned"
    ticket_mentioned = "ticket_mentioned"
    ticket_updated = "ticket_updated"
    ticket_commented = "ticket_commented"
    sprint_started = "sprint_started"
    sprint_completed = "sprint_completed"
    workspace_invited = "workspace_invited"


class Notification(Base, TimestampMixin):
    """Notification model - user notifications."""
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    notification_type: Mapped[NotificationType] = mapped_column(
        String(50), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(String(1000), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # Additional metadata
    action_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notifications")
