import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class SprintStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    completed = "completed"


class Sprint(Base, TimestampMixin):
    """Sprint model - Scrum sprint container."""
    __tablename__ = "sprints"

    board_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[SprintStatus] = mapped_column(
        Enum(SprintStatus), default=SprintStatus.planning, nullable=False
    )

    # Relationships
    board: Mapped["Board"] = relationship(back_populates="sprints")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="sprint")
