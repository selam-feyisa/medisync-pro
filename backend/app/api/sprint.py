from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Sprint, Board, Ticket, Column
from app.models.sprint import SprintStatus
from app.models.ticket import TicketStatus
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/sprints", tags=["sprints"])


class SprintCreate(BaseModel):
    board_id: UUID
    name: str
    goal: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SprintUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_sprint(
    request: SprintCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create new sprint in board."""
    board = await db.get(Board, request.board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    sprint = Sprint(
        board_id=request.board_id,
        name=request.name,
        goal=request.goal,
        start_date=request.start_date,
        end_date=request.end_date,
        status=SprintStatus.planning,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.get("", response_model=list[dict])
async def list_sprints(
    board_id: UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all sprints, optionally filtered by board."""
    if board_id:
        result = await db.execute(
            select(Sprint).where(Sprint.board_id == board_id)
        )
    else:
        result = await db.execute(select(Sprint))
    return result.scalars().all()


@router.get("/{sprint_id}", response_model=dict)
async def get_sprint(
    sprint_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get sprint by ID."""
    sprint = await db.get(Sprint, sprint_id)
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint not found",
        )
    return sprint


@router.patch("/{sprint_id}/start", response_model=dict)
async def start_sprint(
    sprint_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start sprint - change status to active and set start date."""
    sprint = await db.get(Sprint, sprint_id)
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint not found",
        )
    
    if sprint.status != SprintStatus.planning:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only planning sprints can be started",
        )
    
    # Validate no other active sprint exists for this board
    result = await db.execute(
        select(Sprint).where(
            Sprint.board_id == sprint.board_id,
            Sprint.status == SprintStatus.active
        )
    )
    active_sprint = result.scalar_one_or_none()
    if active_sprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Board already has an active sprint",
        )
    
    sprint.status = SprintStatus.active
    sprint.start_date = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.patch("/{sprint_id}/complete", response_model=dict)
async def complete_sprint(
    sprint_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Complete sprint - change status to completed and set end date."""
    sprint = await db.get(Sprint, sprint_id)
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint not found",
        )
    
    if sprint.status != SprintStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active sprints can be completed",
        )
    
    # Find or create backlog column
    result = await db.execute(
        select(Column).where(
            Column.board_id == sprint.board_id,
            Column.position == 0
        )
    )
    backlog_column = result.scalar_one_or_none()
    
    if not backlog_column:
        # Create backlog column
        backlog_column = Column(
            board_id=sprint.board_id,
            name="Backlog",
            position=0,
            is_done_column=False
        )
        db.add(backlog_column)
        await db.flush()
    
    # Move incomplete tickets to backlog
    incomplete_tickets = await db.execute(
        select(Ticket).where(
            Ticket.sprint_id == sprint_id,
            Ticket.status != TicketStatus.DONE
        )
    )
    for ticket in incomplete_tickets.scalars():
        ticket.column_id = backlog_column.id
        ticket.sprint_id = None
    
    sprint.status = SprintStatus.completed
    sprint.end_date = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(sprint)
    return sprint
