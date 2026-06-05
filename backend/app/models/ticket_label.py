import uuid
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class TicketLabel(Base, TimestampMixin):
    """TicketLabel model - M2M between Ticket and Label."""
    __tablename__ = "ticket_labels"
    __table_args__ = (
        UniqueConstraint("ticket_id", "label_id", name="uq_ticket_label"),
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False
    )
    label_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("labels.id"), nullable=False
    )

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="labels")
    label: Mapped["Label"] = relationship(back_populates="tickets")
