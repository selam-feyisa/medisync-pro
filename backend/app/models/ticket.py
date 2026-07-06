from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLEnum, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum

from app.models.base import Base, TimestampMixin


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

    


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.TODO)
    position = Column(Integer, default=0)
    due_date = Column(DateTime)
    story_points = Column(Float, default=0.0)
    
    column_id = Column(UUID(as_uuid=True), ForeignKey("columns.id", ondelete="CASCADE"))
    sprint_id = Column(UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # === NEW: Full-Text Search ===
    search_vector = Column(Text)   # tsvector will be handled in migration later

    # Relationships
    column = relationship("Column", back_populates="tickets")
    sprint = relationship("Sprint", back_populates="tickets")
    created_by = relationship("User")
    assignees = relationship("TicketAssignee", back_populates="ticket", cascade="all, delete-orphan")
    labels = relationship("TicketLabel", back_populates="ticket", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="ticket", cascade="all, delete-orphan")

    # ==================== Full-Text Search Event Listener ====================
from sqlalchemy import event
import sqlalchemy as sa


@event.listens_for(Ticket, 'before_insert')
@event.listens_for(Ticket, 'before_update')
def update_search_vector(mapper, connection, target):
    """Automatically update search_vector before save for full-text search"""
    search_text = f"{target.title or ''} {target.description or ''}".strip()
    if search_text:
        target.search_vector = sa.func.to_tsvector('english', search_text)