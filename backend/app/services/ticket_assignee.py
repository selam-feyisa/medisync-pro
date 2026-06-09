from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from backend.app.models.ticket_assignee import TicketAssignee
from backend.app.core.exceptions import NotFoundException


async def add_assignee(db: AsyncSession, ticket_id: UUID, user_id: UUID) -> TicketAssignee:
    assignee = TicketAssignee(ticket_id=ticket_id, user_id=user_id)
    db.add(assignee)
    await db.commit()
    await db.refresh(assignee)
    return assignee


async def remove_assignee(db: AsyncSession, ticket_id: UUID, user_id: UUID) -> bool:
    result = await db.execute(
        select(TicketAssignee).where(
            TicketAssignee.ticket_id == ticket_id,
            TicketAssignee.user_id == user_id
        )
    )
    assignee = result.scalar_one_or_none()
    if not assignee:
        raise NotFoundException("Assignee not found")
    
    await db.delete(assignee)
    await db.commit()
    return True