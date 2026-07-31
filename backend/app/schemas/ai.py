"""AI-related schemas for requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AIRequest(BaseModel):
    """Base schema for AI requests."""
    operation_type: str = Field(..., description="Type of AI operation")
    model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")


class TicketSummarizeRequest(AIRequest):
    """Request schema for ticket summarization."""
    operation_type: str = "ticket_summarize"
    ticket_id: str = Field(..., description="ID of the ticket to summarize")
    include_comments: bool = Field(default=True, description="Include comments in summary")


class PRDescriptionRequest(AIRequest):
    """Request schema for PR/workspace description generation."""
    operation_type: str = "pr_description"
    workspace_id: str = Field(..., description="ID of the workspace")
    context: str = Field(default="", description="Additional context for description")


class AIResponse(BaseModel):
    """Base schema for AI responses."""
    operation_type: str
    result: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    model_used: str


class AIUsageLogResponse(BaseModel):
    """Response schema for AI usage log entries."""
    id: str
    workspace_id: str
    user_id: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    operation_type: str
    model_used: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkspaceAIQuotaResponse(BaseModel):
    """Response schema for workspace AI quota."""
    id: str
    workspace_id: str
    monthly_limit: int
    used_tokens: int
    remaining_tokens: int
    current_period_start: datetime
    current_period_end: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True
