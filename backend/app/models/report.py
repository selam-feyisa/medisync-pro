import uuid
import enum
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class ReportType(str, enum.Enum):
    sprint_burndown = "sprint_burndown"
    velocity = "velocity"
    time_tracking = "time_tracking"
    ticket_distribution = "ticket_distribution"
    custom = "custom"


class Report(Base, TimestampMixin):
    """Report model - saved analytics reports."""
    __tablename__ = "reports"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[ReportType] = mapped_column(String(50), nullable=False)
    filters: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # Report filters
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # Report configuration
    is_public: Mapped[bool] = mapped_column(default=False)  # Share with workspace

    # Relationships
    workspace: Mapped["Workspace"] = relationship
    created_by: Mapped["User"] = relationship
