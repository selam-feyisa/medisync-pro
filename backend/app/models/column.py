import uuid
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Column(Base, TimestampMixin):
    """Column model - swimlane in Kanban board."""
    __tablename__ = "columns"

    board_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_done_column: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    board: Mapped["Board"] = relationship(back_populates="columns")
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="column", cascade="all, delete-orphan"
    )
