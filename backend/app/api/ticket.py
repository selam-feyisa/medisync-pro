from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate, TicketUpdate, TicketResponse, 
    TicketMove, TicketListResponse
)
from app.services.ticket import (
    create_ticket, get_tickets_by_column, 
    update_ticket, move_ticket, delete_ticket
)

router = APIRouter()


class BulkUpdate(BaseModel):
    ticket_ids: List[UUID]
    updates: dict


class BulkMove(BaseModel):
    ticket_ids: List[UUID]
    column_id: UUID
    position: int = 0

@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_new_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = await create_ticket(db, ticket_data, current_user.id)
    return ticket


@router.get("/columns/{column_id}/tickets", response_model=List[TicketResponse])
async def list_column_tickets(
    column_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tickets = await get_tickets_by_column(db, column_id)
    return tickets


@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_existing_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = await update_ticket(db, ticket_id, ticket_data, current_user.id)
    return ticket


@router.patch("/tickets/{ticket_id}/move", response_model=TicketResponse)
async def move_existing_ticket(
    ticket_id: UUID,
    move_data: TicketMove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = await move_ticket(db, ticket_id, move_data, current_user.id)
    return ticket


@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await delete_ticket(db, ticket_id)
    return None


@router.patch("/tickets/bulk/update", response_model=List[TicketResponse])
async def bulk_update_tickets(
    request: BulkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk update multiple tickets with same changes."""
    from app.models.ticket import Ticket
    from sqlalchemy import select
    
    updated_tickets = []
    for ticket_id in request.ticket_ids:
        ticket = await db.get(Ticket, ticket_id)
        if ticket:
            for key, value in request.updates.items():
                setattr(ticket, key, value)
            updated_tickets.append(ticket)
    
    await db.commit()
    
    for ticket in updated_tickets:
        await db.refresh(ticket)
    
    return updated_tickets


@router.patch("/tickets/bulk/move", response_model=List[TicketResponse])
async def bulk_move_tickets(
    request: BulkMove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk move multiple tickets to same column."""
    from app.models.ticket import Ticket
    from sqlalchemy import select
    
    moved_tickets = []
    position_offset = 0
    
    for idx, ticket_id in enumerate(request.ticket_ids):
        ticket = await db.get(Ticket, ticket_id)
        if ticket:
            ticket.column_id = request.column_id
            ticket.position = request.position + (idx * 1000)
            moved_tickets.append(ticket)
    
    await db.commit()
    
    for ticket in moved_tickets:
        await db.refresh(ticket)
    
    return moved_tickets