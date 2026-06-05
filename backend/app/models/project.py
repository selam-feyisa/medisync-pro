import uuid
import enum
from sqlalchemy import String, Text, Boolean, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Visibility(str, enum.Enum):
    public = "public"
    private = "private"


class Project(Base, TimestampMixin):
    """Project model - container for boards and tickets."""
    __tablename__ = "projects"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[Visibility] = mapped_column(
        Enum(Visibility), default=Visibility.private, nullable=False
    )
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship(back_populates="projects")
    boards: Mapped[list["Board"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
