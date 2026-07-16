from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Ticket, TicketActivity

router = APIRouter(prefix="/tickets/{ticket_id}/activities", tags=["ticket-activities"])


@router.get("", response_model=List[TicketActivity])
async def list_ticket_activities(
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TicketActivity]:
    """List all activities for a ticket in chronological order."""
    # Verify ticket exists
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    result = await db.execute(
        select(TicketActivity)
        .where(TicketActivity.ticket_id == ticket_id)
        .order_by(TicketActivity.created_at.desc())
    )
    return result.scalars().all()
