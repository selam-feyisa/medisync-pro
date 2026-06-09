from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import List, Optional

from backend.app.models.ticket import Ticket, TicketPriority, TicketStatus
from backend.app.models.ticket_assignee import TicketAssignee
from backend.app.models.ticket_label import TicketLabel
from backend.app.schemas.ticket import TicketCreate, TicketUpdate, TicketMove
from backend.app.core.exceptions import NotFoundException, PermissionException


async def get_tickets_by_column(db: AsyncSession, column_id: UUID) -> List[Ticket]:
    result = await db.execute(
        select(Ticket)
        .options(joinedload(Ticket.assignees), joinedload(Ticket.labels))
        .where(Ticket.column_id == column_id)
        .order_by(Ticket.position)
    )
    return result.scalars().all()


async def create_ticket(db: AsyncSession, data: TicketCreate, user_id: UUID) -> Ticket:
    # Auto position (gap strategy)
    max_pos_result = await db.execute(
        select(Ticket.position).where(Ticket.column_id == data.column_id).order_by(desc(Ticket.position)).limit(1)
    )
    max_pos = max_pos_result.scalar() or 0
    position = max_pos + 1000

    ticket = Ticket(
        **data.dict(),
        created_by_id=user_id,
        position=position
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def update_ticket(db: AsyncSession, ticket_id: UUID, data: TicketUpdate) -> Ticket:
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise NotFoundException("Ticket not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    await db.commit()
    await db.refresh(ticket)
    return ticket


async def move_ticket(db: AsyncSession, ticket_id: UUID, move_data: TicketMove) -> Ticket:
    """Move ticket to new column with position gap strategy"""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise NotFoundException("Ticket not found")

    ticket.column_id = move_data.column_id
    ticket.position = move_data.position

    await db.commit()
    await db.refresh(ticket)
    return ticket


async def delete_ticket(db: AsyncSession, ticket_id: UUID) -> bool:
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise NotFoundException("Ticket not found")
    
    await db.delete(ticket)
    await db.commit()
    return True