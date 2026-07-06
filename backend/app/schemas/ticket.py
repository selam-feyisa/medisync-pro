from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.models.ticket import TicketPriority, TicketStatus

class TicketBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.TODO
    due_date: Optional[datetime] = None
    story_points: Optional[float] = Field(0.0, ge=0)
    position: Optional[int] = 0

class TicketCreate(TicketBase):
    column_id: UUID

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    due_date: Optional[datetime] = None
    story_points: Optional[float] = None
    position: Optional[int] = None
    column_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None

class TicketResponse(TicketBase):
    id: UUID
    column_id: UUID
    sprint_id: Optional[UUID] = None
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TicketMove(BaseModel):
    column_id: UUID
    position: int

class TicketListResponse(BaseModel):
    items: List[TicketResponse]
    total: int