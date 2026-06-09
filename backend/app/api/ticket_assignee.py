from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.services.ticket_assignee import add_assignee, remove_assignee

router = APIRouter(prefix="/tickets", tags=["Ticket Assignees"])

@router.post("/{ticket_id}/assignees/{user_id}", status_code=status.HTTP_201_CREATED)
async def add_ticket_assignee(
    ticket_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await add_assignee(db, ticket_id, user_id)
    return {"message": "Assignee added successfully"}


@router.delete("/{ticket_id}/assignees/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_ticket_assignee(
    ticket_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await remove_assignee(db, ticket_id, user_id)
    return None