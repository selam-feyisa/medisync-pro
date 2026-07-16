from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

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