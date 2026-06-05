from pydantic import BaseModel
from typing import Optional
import uuid


class WorkspaceBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspacePatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    plan: Optional[str] = None


class WorkspaceResponse(WorkspaceBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    plan: str

    class Config:
        from_attributes = True


class WorkspaceDetailResponse(WorkspaceResponse):
    members_count: int
    projects_count: int
