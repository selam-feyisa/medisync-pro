from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CommentBase(BaseModel):
    body: str = Field(..., min_length=1, max_length=2000)
    parent_id: Optional[UUID] = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID
    ticket_id: UUID
    author_id: UUID
    is_edited: bool = False
    created_at: datetime
    updated_at: datetime
    replies: List['CommentResponse'] = []

    class Config:
        from_attributes = True