import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class AIUsageLog(Base, TimestampMixin):
    """AI usage tracking model for token and cost logging."""
    __tablename__ = "ai_usage_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Token usage
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    
    # Cost tracking
    cost = Column(Float, nullable=False, default=0.0)
    
    # Operation details
    operation_type = Column(String(50), nullable=False)  # e.g., "ticket_summarize", "pr_description"
    model_used = Column(String(50), nullable=False)  # e.g., "gpt-4", "gpt-3.5-turbo"
    
    # Relationships
    workspace = relationship("Workspace")
    user = relationship("User")

    def __repr__(self):
        return f"<AIUsageLog {self.id} - {self.operation_type} - {self.total_tokens} tokens>"
