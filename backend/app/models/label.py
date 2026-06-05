import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Label(Base, TimestampMixin):
    """Label model - workspace-level labels."""
    __tablename__ = "labels"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)  # hex color code

    # Relationships
    tickets: Mapped[list["TicketLabel"]] = relationship(
        back_populates="label", cascade="all, delete-orphan"
    )
