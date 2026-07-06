from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class LabelBase(BaseModel):
    workspace_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    color: str = Field(..., min_length=4, max_length=7)


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    color: Optional[str] = Field(None, min_length=4, max_length=7)


class LabelResponse(LabelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
