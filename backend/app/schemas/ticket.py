from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "todo"
    story_points: Optional[int] = None
    due_date: Optional[datetime] = None


class TicketCreate(TicketBase):
    column_id: uuid.UUID
    position: int


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    story_points: Optional[int] = None
    due_date: Optional[datetime] = None
    column_id: Optional[uuid.UUID] = None


class TicketMove(BaseModel):
    column_id: uuid.UUID
    position: int


class TicketResponse(TicketBase):
    id: uuid.UUID
    column_id: uuid.UUID
    position: int

    class Config:
        from_attributes = True


class TicketDetailResponse(TicketResponse):
    assignees: list[uuid.UUID] = []
    labels: list[uuid.UUID] = []
    comments_count: int = 0
    attachments_count: int = 0
