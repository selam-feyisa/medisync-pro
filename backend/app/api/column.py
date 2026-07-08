from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Column, Board
from app.schemas import ColumnCreate, ColumnResponse, ColumnUpdate

router = APIRouter(prefix="/columns", tags=["columns"])


class ColumnReorder(BaseModel):
    columns: List[dict]  # [{"id": uuid, "position": int}]


@router.post("", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
async def create_column(
    request: ColumnCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Column:
    """Create new column in board."""
    board = await db.get(Board, request.board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    column = Column(
        board_id=request.board_id,
        name=request.name,
        position=request.position,
        is_done_column=request.is_done_column,
    )
    db.add(column)
    await db.commit()
    await db.refresh(column)
    return column


@router.get("/{column_id}", response_model=ColumnResponse)
async def get_column(
    column_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Column:
    """Get column by ID."""
    column = await db.get(Column, column_id)
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )
    return column


@router.patch("/{column_id}", response_model=ColumnResponse)
async def update_column(
    column_id: UUID,
    request: ColumnUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Column:
    """Update column details."""
    column = await db.get(Column, column_id)
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )

    if request.name:
        column.name = request.name
    if request.position is not None:
        column.position = request.position
    if request.is_done_column is not None:
        column.is_done_column = request.is_done_column

    await db.commit()
    return column


@router.delete("/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column(
    column_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete column (soft delete)."""
    column = await db.get(Column, column_id)
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )
    await db.delete(column)
    await db.commit()


@router.patch("/boards/{board_id}/columns/reorder", response_model=list[ColumnResponse])
async def reorder_columns(
    board_id: UUID,
    request: ColumnReorder,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Column]:
    """Bulk update column positions in a board."""
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    for col_data in request.columns:
        column = await db.get(Column, col_data["id"])
        if column and column.board_id == board_id:
            column.position = col_data["position"]

    await db.commit()
    
    result = await db.execute(
        select(Column).where(Column.board_id == board_id).order_by(Column.position)
    )
    return result.scalars().all()
