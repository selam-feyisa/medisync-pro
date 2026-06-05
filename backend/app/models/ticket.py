import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TicketStatus(str, enum.Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"


class Ticket(Base, TimestampMixin):
    """Ticket model - atomic unit of work."""
    __tablename__ = "tickets"

    column_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("columns.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority), default=Priority.medium, nullable=False
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.todo, nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    story_points: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    column: Mapped["Column"] = relationship(back_populates="tickets")
    assignees: Mapped[list["TicketAssignee"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )
    labels: Mapped[list["TicketLabel"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )
    attachments: Mapped[list["FileAttachment"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )
