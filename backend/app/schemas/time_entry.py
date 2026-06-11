from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from backend.app.constants import TimeEntryStatus  # We'll add this later if needed

class TimeEntryBase(BaseModel):
    description: Optional[str] = None
    is_billable: bool = True
    ticket_id: Optional[UUID] = None

class TimeEntryStart(BaseModel):
    ticket_id: Optional[UUID] = None
    description: Optional[str] = None

class TimeEntryStop(BaseModel):
    description: Optional[str] = None

class TimeEntryResponse(TimeEntryBase):
    id: UUID
    workspace_id: UUID
    user_id: UUID
    started_at: datetime
    stopped_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    status: str

    class Config:
        from_attributes = True