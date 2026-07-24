import uuid
import enum
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class TicketActivityType(str, enum.Enum):
    created = "created"
    updated = "updated"
    moved = "moved"
    commented = "commented"
    assigned = "assigned"


class TicketActivity(Base, TimestampMixin):
    """TicketActivity model - tracks all ticket changes."""
    __tablename__ = "ticket_activities"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    action: Mapped[TicketActivityType] = mapped_column(
        String(50), nullable=False
    )
    old_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="activities")
    user: Mapped["User"] = relationship
