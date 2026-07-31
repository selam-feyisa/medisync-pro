"""v2 API schemas with camelCase formatting."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TicketResponseV2(BaseModel):
    """Ticket response schema with camelCase fields."""
    id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    position: int
    dueDate: Optional[datetime] = None
    storyPoints: Optional[float] = None
    columnId: str
    sprintId: Optional[str] = None
    createdById: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class TicketCreateV2(BaseModel):
    """Ticket creation schema with camelCase fields."""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "todo"
    position: int = 0
    dueDate: Optional[datetime] = None
    storyPoints: Optional[float] = None
    columnId: str
    sprintId: Optional[str] = None


class TicketUpdateV2(BaseModel):
    """Ticket update schema with camelCase fields."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    position: Optional[int] = None
    dueDate: Optional[datetime] = None
    storyPoints: Optional[float] = None
    columnId: Optional[str] = None
    sprintId: Optional[str] = None


class WorkspaceResponseV2(BaseModel):
    """Workspace response schema with camelCase fields."""
    id: str
    name: str
    slug: str
    ownerId: str
    planType: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class ProjectResponseV2(BaseModel):
    """Project response schema with camelCase fields."""
    id: str
    workspaceId: str
    name: str
    slug: str
    description: Optional[str] = None
    visibility: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class BoardResponseV2(BaseModel):
    """Board response schema with camelCase fields."""
    id: str
    projectId: str
    name: str
    boardType: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class ColumnResponseV2(BaseModel):
    """Column response schema with camelCase fields."""
    id: str
    boardId: str
    name: str
    position: int
    
    class Config:
        from_attributes = True
        populate_by_name = True


class SprintResponseV2(BaseModel):
    """Sprint response schema with camelCase fields."""
    id: str
    boardId: str
    name: str
    goal: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    status: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
