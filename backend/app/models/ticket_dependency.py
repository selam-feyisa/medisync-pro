import uuid
import enum
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class DependencyType(str, enum.Enum):
    blocks = "blocks"
    relates_to = "relates_to"
    duplicates = "duplicates"


class TicketDependency(Base, TimestampMixin):
    """TicketDependency model - relationships between tickets."""
    __tablename__ = "ticket_dependencies"

    blocker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    blocked_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    dependency_type: Mapped[DependencyType] = mapped_column(
        String(50), default=DependencyType.blocks, nullable=False
    )

    # Relationships
    blocker: Mapped["Ticket"] = relationship(
        foreign_keys=[blocker_id]
        # back_populates="blocking_dependencies"
    )
    blocked: Mapped["Ticket"] = relationship(
        foreign_keys=[blocked_id]
        # back_populates="blocked_dependencies"
    )
