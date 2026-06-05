from pydantic import BaseModel
from typing import Optional
import uuid


class ColumnBase(BaseModel):
    name: str
    position: int
    is_done_column: bool = False


class ColumnCreate(ColumnBase):
    board_id: uuid.UUID


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None
    is_done_column: Optional[bool] = None


class ColumnResponse(ColumnBase):
    id: uuid.UUID
    board_id: uuid.UUID

    class Config:
        from_attributes = True


class BoardBase(BaseModel):
    name: str
    board_type: str = "kanban"


class BoardCreate(BoardBase):
    project_id: uuid.UUID


class BoardUpdate(BaseModel):
    name: Optional[str] = None
    board_type: Optional[str] = None


class BoardResponse(BoardBase):
    id: uuid.UUID
    project_id: uuid.UUID

    class Config:
        from_attributes = True


class BoardDetailResponse(BoardResponse):
    columns: list[ColumnResponse] = []
