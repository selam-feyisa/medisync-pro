"""AI API endpoints for ticket summarization and PR description generation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import (
    TicketSummarizeRequest,
    PRDescriptionRequest,
    AIResponse
)
from app.services.ai_service import get_ai_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/tickets/{ticket_id}/summarize", response_model=AIResponse)
async def summarize_ticket(
    ticket_id: str,
    request: TicketSummarizeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate an AI summary for a ticket."""
    ai_service = get_ai_service()
    if not ai_service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="AI service not configured"
        )
    
    try:
        result = await ai_service.summarize_ticket(
            ticket_id=ticket_id,
            include_comments=request.include_comments,
            workspace_id=request.workspace_id,  # Will need to be derived from ticket
            user_id=str(current_user.id),
            db=db
        )
        await db.commit()
        return AIResponse(**result)
    except Exception as e:
        await db.rollback()
        if "quota" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="AI token quota exceeded"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI operation failed: {str(e)}"
        )


@router.post("/workspaces/{workspace_id}/pr-description", response_model=AIResponse)
async def generate_pr_description(
    workspace_id: str,
    request: PRDescriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate an AI PR/workspace description."""
    ai_service = get_ai_service()
    if not ai_service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="AI service not configured"
        )
    
    try:
        result = await ai_service.generate_pr_description(
            workspace_id=workspace_id,
            context=request.context,
            user_id=str(current_user.id),
            db=db
        )
        await db.commit()
        return AIResponse(**result)
    except Exception as e:
        await db.rollback()
        if "quota" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="AI token quota exceeded"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI operation failed: {str(e)}"
        )
