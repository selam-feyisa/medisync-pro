from pydantic import BaseModel
from typing import Optional
import uuid


class ProjectBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    visibility: str = "private"


class ProjectCreate(ProjectBase):
    workspace_id: uuid.UUID


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None
    is_archived: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    is_archived: bool

    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    boards_count: int
