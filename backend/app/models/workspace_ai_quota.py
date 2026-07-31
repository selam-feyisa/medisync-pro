import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class WorkspaceAIQuota(Base, TimestampMixin):
    """AI quota tracking model for workspaces."""
    __tablename__ = "workspace_ai_quotas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False, unique=True)
    
    # Monthly token limit
    monthly_limit = Column(Integer, nullable=False, default=100000)  # Default 100k tokens/month
    
    # Usage tracking
    used_tokens = Column(Integer, nullable=False, default=0)
    
    # Period tracking
    current_period_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    current_period_end = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Integer, nullable=False, default=1)  # 1 = active, 0 = disabled
    
    # Relationships
    workspace = relationship("Workspace")

    def __repr__(self):
        return f"<WorkspaceAIQuota {self.workspace_id} - {self.used_tokens}/{self.monthly_limit} tokens>"
    
    @property
    def remaining_tokens(self) -> int:
        """Calculate remaining tokens for the current period."""
        return max(0, self.monthly_limit - self.used_tokens)
    
    @property
    def is_quota_exceeded(self) -> bool:
        """Check if quota has been exceeded."""
        return self.used_tokens >= self.monthly_limit
