from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Ticket, Column
from app.schemas import TicketCreate, TicketResponse, TicketUpdate, TicketMove

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    request: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ticket:
    """Create new ticket."""
    column = await db.get(Column, request.column_id)
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )

    ticket = Ticket(
        column_id=request.column_id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        status=request.status,
        position=request.position,
        story_points=request.story_points,
        due_date=request.due_date,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ticket:
    """Get ticket by ID."""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: UUID,
    request: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Ticket:
    """Update ticket details."""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if request.title:
        ticket.title = request.title
    if request.description is not None:
        ticket.description = request.description
    if request.priority:
        ticket.priority = request.priority
    if request.status:
        ticket.status = request.status
    if request.story_points is not None:
        ticket.story_points = request.story_points
    if request.due_date:
        ticket.due_date = request.due_date

    await db.commit()
    return ticket


@router.post("/{ticket_id}/move")
async def move_ticket(
    ticket_id: UUID,
    request: TicketMove,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Move ticket to different column."""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    ticket.column_id = request.column_id
    ticket.position = request.position
    await db.commit()
    return {"message": "Ticket moved successfully"}


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete ticket (soft delete)."""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    await db.delete(ticket)
    await db.commit()
