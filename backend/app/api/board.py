from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Board, Project
from app.schemas import BoardCreate, BoardResponse, BoardUpdate

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    request: BoardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Board:
    """Create new board."""
    project = await db.get(Project, request.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    board = Board(
        project_id=request.project_id,
        name=request.name,
        board_type=request.board_type,
    )
    db.add(board)
    await db.commit()
    await db.refresh(board)
    return board


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Board:
    """Get board by ID."""
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )
    return board


@router.patch("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: UUID,
    request: BoardUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Board:
    """Update board details."""
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    if request.name:
        board.name = request.name
    if request.board_type:
        board.board_type = request.board_type

    await db.commit()
    return board
