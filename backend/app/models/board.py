import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class BoardType(str, enum.Enum):
    kanban = "kanban"
    scrum = "scrum"


class Board(Base, TimestampMixin):
    """Board model - Kanban or Scrum board."""
    __tablename__ = "boards"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    board_type: Mapped[BoardType] = mapped_column(
        Enum(BoardType), default=BoardType.kanban, nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="boards")
    columns: Mapped[list["Column"]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )
    sprints: Mapped[list["Sprint"]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )
