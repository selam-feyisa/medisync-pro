from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class TimeEntryBase(BaseModel):
    description: Optional[str] = None
    is_billable: bool = True
    ticket_id: Optional[UUID] = None


class TimeEntryStart(TimeEntryBase):
    pass


class TimeEntryManual(BaseModel):
    ticket_id: Optional[UUID] = None
    started_at: datetime
    stopped_at: datetime
    description: Optional[str] = None
    is_billable: bool = True


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