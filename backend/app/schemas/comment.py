from pydantic import BaseModel
from typing import Optional
import uuid


class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    ticket_id: uuid.UUID
    parent_id: Optional[uuid.UUID] = None


class CommentUpdate(BaseModel):
    body: Optional[str] = None


class CommentResponse(CommentBase):
    id: uuid.UUID
    ticket_id: uuid.UUID
    author_id: uuid.UUID
    is_edited: bool
    parent_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class LabelBase(BaseModel):
    name: str
    color: str


class LabelCreate(LabelBase):
    workspace_id: uuid.UUID


class LabelUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class LabelResponse(LabelBase):
    id: uuid.UUID
    workspace_id: uuid.UUID

    class Config:
        from_attributes = True
