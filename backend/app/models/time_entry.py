from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum

from app.models.base import Base, TimestampMixin


class TimeEntryStatus(str, Enum):
    RUNNING = "running"
    LOGGED = "logged"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class TimeEntry(Base, TimestampMixin):
    __tablename__ = "time_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    started_at = Column(DateTime, nullable=False)
    stopped_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    description = Column(String(500))
    is_billable = Column(Boolean, default=True)
    status = Column(SQLEnum(TimeEntryStatus), default=TimeEntryStatus.RUNNING)

    # Relationships
    ticket = relationship("Ticket")
    user = relationship("User")

    def __repr__(self):
        return f"<TimeEntry {self.id} - {self.status}>"