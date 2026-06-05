import uuid
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class TicketAssignee(Base, TimestampMixin):
    """TicketAssignee model - M2M between Ticket and User."""
    __tablename__ = "ticket_assignees"
    __table_args__ = (
        UniqueConstraint("ticket_id", "user_id", name="uq_ticket_user"),
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="assignees")
    user: Mapped["User"] = relationship()
