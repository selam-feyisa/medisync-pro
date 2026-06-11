from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.services.search import search_tickets
from backend.app.schemas.ticket import TicketResponse

router = APIRouter()

@router.get("/workspaces/{workspace_id}/search", response_model=List[TicketResponse])
async def search_workspace(
    workspace_id: UUID,
    q: str = Query(..., min_length=2, description="Search query"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Full-text search across tickets in a workspace"""
    try:
        tickets = await search_tickets(db, workspace_id, q)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")