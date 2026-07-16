from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc, and_
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import List, Optional

from app.models.ticket import Ticket, TicketPriority, TicketStatus
from app.models.ticket_assignee import TicketAssignee
from app.models.ticket_label import TicketLabel
from app.models.audit_log import AuditLog
from app.models.ticket_activity import TicketActivity, TicketActivityType
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketMove
from app.core.exceptions import NotFoundException, PermissionException


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
    await db.flush()

    # Auto-log creation activity
    activity = TicketActivity(
        ticket_id=ticket.id,
        user_id=user_id,
        action=TicketActivityType.created,
        old_value=None,
        new_value={"title": ticket.title, "priority": ticket.priority.value}
    )
    db.add(activity)

    await db.commit()
    await db.refresh(ticket)
    return ticket


async def update_ticket(db: AsyncSession, ticket_id: UUID, data: TicketUpdate, user_id: UUID) -> Ticket:
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise NotFoundException("Ticket not found")

    old_values = {}
    new_values = {}
    
    for key, value in data.dict(exclude_unset=True).items():
        old_values[key] = getattr(ticket, key)
        setattr(ticket, key, value)
        new_values[key] = value

    await db.flush()

    # Auto-log update activity if changes were made
    if old_values:
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=user_id,
            action=TicketActivityType.updated,
            old_value=old_values,
            new_value=new_values
        )
        db.add(activity)

    await db.commit()
    await db.refresh(ticket)
    return ticket


async def move_ticket(db: AsyncSession, ticket_id: UUID, move_data: TicketMove, user_id: UUID) -> Ticket:
    """Move ticket to new column with position gap strategy"""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise NotFoundException("Ticket not found")

    from_column_id = ticket.column_id
    to_column_id = move_data.column_id
    target_position = move_data.position

    # Get neighbours in target column
    neighbours = await db.execute(
        select(Ticket)
        .where(Ticket.column_id == to_column_id)
        .where(Ticket.id != ticket_id)
        .order_by(Ticket.position)
    )
    neighbour_tickets = neighbours.scalars().all()

    # Find position between neighbours
    prev_pos = 0
    next_pos = None
    for nt in neighbour_tickets:
        if nt.position < target_position:
            prev_pos = nt.position
        elif nt.position > target_position:
            next_pos = nt.position
            break

    # Check gap size
    gap = (next_pos - prev_pos) if next_pos else 1000

    if gap > 2:
        # Insert in gap
        new_position = prev_pos + (gap // 2)
    else:
        # Rebalance entire column with 1000-gap strategy
        all_tickets = await db.execute(
            select(Ticket)
            .where(Ticket.column_id == to_column_id)
            .order_by(Ticket.position)
        )
        column_tickets = all_tickets.scalars().all()
        
        # Add moving ticket to list
        if ticket not in column_tickets:
            column_tickets.append(ticket)
        
        # Sort by target position
        column_tickets.sort(key=lambda t: t.position if t.id == ticket_id else t.position)
        
        # Reassign positions with 1000 gaps
        for idx, t in enumerate(column_tickets):
            t.position = idx * 1000
            if t.id == ticket_id:
                new_position = t.position

    ticket.column_id = to_column_id
    ticket.position = new_position

    # Log move in AuditLog
    audit_log = AuditLog(
        workspace_id=ticket.column.board.project.workspace_id if ticket.column else None,
        actor_id=user_id,
        action="ticket.moved",
        resource_type="ticket",
        resource_id=ticket_id,
        metadata={"from_column": str(from_column_id), "to_column": str(to_column_id)}
    )
    db.add(audit_log)

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