from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.services.ticket_label import add_label, remove_label

router = APIRouter(prefix="/tickets", tags=["Ticket Labels"])

@router.post("/{ticket_id}/labels/{label_id}", status_code=status.HTTP_201_CREATED)
async def add_ticket_label(
    ticket_id: UUID,
    label_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await add_label(db, ticket_id, label_id)
    return {"message": "Label attached successfully"}


@router.delete("/{ticket_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_ticket_label(
    ticket_id: UUID,
    label_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await remove_label(db, ticket_id, label_id)
    return None