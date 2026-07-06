from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.ticket_label import TicketLabel
from app.core.exceptions import NotFoundException


async def add_label(db: AsyncSession, ticket_id: UUID, label_id: UUID) -> TicketLabel:
    ticket_label = TicketLabel(ticket_id=ticket_id, label_id=label_id)
    db.add(ticket_label)
    await db.commit()
    await db.refresh(ticket_label)
    return ticket_label


async def remove_label(db: AsyncSession, ticket_id: UUID, label_id: UUID) -> bool:
    result = await db.execute(
        select(TicketLabel).where(
            TicketLabel.ticket_id == ticket_id,
            TicketLabel.label_id == label_id
        )
    )
    ticket_label = result.scalar_one_or_none()
    if not ticket_label:
        raise NotFoundException("Label not found on ticket")
    
    await db.delete(ticket_label)
    await db.commit()
    return True