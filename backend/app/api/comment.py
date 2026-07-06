from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment import create_comment, get_ticket_comments

router = APIRouter()

@router.post("/tickets/{ticket_id}/comments", 
             response_model=CommentResponse, 
             status_code=status.HTTP_201_CREATED)
async def create_new_comment(
    ticket_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new comment with mention parsing support"""
    comment = await create_comment(db, ticket_id, comment_data, current_user.id)
    return comment


@router.get("/tickets/{ticket_id}/comments", 
            response_model=List[CommentResponse])
async def list_ticket_comments(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all comments for a ticket (including threaded replies)"""
    comments = await get_ticket_comments(db, ticket_id)
    return comments