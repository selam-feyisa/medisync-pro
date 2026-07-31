"""v2 API endpoints for tickets with camelCase formatting."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.ticket import Ticket
from app.models.workspace_member import MemberRole
from app.schemas.v2.ticket import (
    TicketResponseV2,
    TicketCreateV2,
    TicketUpdateV2
)
from app.core.dependencies import require_workspace_role

router = APIRouter(prefix="/tickets", tags=["Tickets v2"])


@router.post("", response_model=TicketResponseV2, status_code=status.HTTP_201_CREATED)
async def create_ticket_v2(
    data: TicketCreateV2,
    workspace_id: str = Query(...),
    current_user: User = Depends(require_workspace_role(MemberRole.nurse)),
    db: AsyncSession = Depends(get_db)
):
    """Create a new ticket (v2 API with camelCase)."""
    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        status=data.status,
        position=data.position,
        due_date=data.dueDate,
        story_points=data.storyPoints,
        column_id=data.columnId,
        sprint_id=data.sprintId,
        created_by_id=str(current_user.id)
    )
    
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    
    return TicketResponseV2(
        id=str(ticket.id),
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority.value,
        status=ticket.status.value,
        position=ticket.position,
        dueDate=ticket.due_date,
        storyPoints=ticket.story_points,
        columnId=str(ticket.column_id),
        sprintId=str(ticket.sprint_id) if ticket.sprint_id else None,
        createdById=str(ticket.created_by_id),
        createdAt=ticket.created_at,
        updatedAt=ticket.updated_at
    )


@router.get("/{ticket_id}", response_model=TicketResponseV2)
async def get_ticket_v2(
    ticket_id: str,
    workspace_id: str = Query(...),
    current_user: User = Depends(require_workspace_role(MemberRole.patient)),
    db: AsyncSession = Depends(get_db)
):
    """Get a ticket by ID (v2 API with camelCase)."""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    return TicketResponseV2(
        id=str(ticket.id),
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority.value,
        status=ticket.status.value,
        position=ticket.position,
        dueDate=ticket.due_date,
        storyPoints=ticket.story_points,
        columnId=str(ticket.column_id),
        sprintId=str(ticket.sprint_id) if ticket.sprint_id else None,
        createdById=str(ticket.created_by_id),
        createdAt=ticket.created_at,
        updatedAt=ticket.updated_at
    )


@router.patch("/{ticket_id}", response_model=TicketResponseV2)
async def update_ticket_v2(
    ticket_id: str,
    data: TicketUpdateV2,
    workspace_id: str = Query(...),
    current_user: User = Depends(require_workspace_role(MemberRole.nurse)),
    db: AsyncSession = Depends(get_db)
):
    """Update a ticket (v2 API with camelCase)."""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Update fields
    if data.title is not None:
        ticket.title = data.title
    if data.description is not None:
        ticket.description = data.description
    if data.priority is not None:
        ticket.priority = data.priority
    if data.status is not None:
        ticket.status = data.status
    if data.position is not None:
        ticket.position = data.position
    if data.dueDate is not None:
        ticket.due_date = data.dueDate
    if data.storyPoints is not None:
        ticket.story_points = data.storyPoints
    if data.columnId is not None:
        ticket.column_id = data.columnId
    if data.sprintId is not None:
        ticket.sprint_id = data.sprintId
    
    await db.commit()
    await db.refresh(ticket)
    
    return TicketResponseV2(
        id=str(ticket.id),
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority.value,
        status=ticket.status.value,
        position=ticket.position,
        dueDate=ticket.due_date,
        storyPoints=ticket.story_points,
        columnId=str(ticket.column_id),
        sprintId=str(ticket.sprint_id) if ticket.sprint_id else None,
        createdById=str(ticket.created_by_id),
        createdAt=ticket.created_at,
        updatedAt=ticket.updated_at
    )


@router.get("", response_model=List[TicketResponseV2])
async def list_tickets_v2(
    workspace_id: str = Query(...),
    column_id: Optional[str] = Query(None),
    sprint_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_workspace_role(MemberRole.patient)),
    db: AsyncSession = Depends(get_db)
):
    """List tickets with filters (v2 API with camelCase)."""
    query = select(Ticket)
    
    if column_id:
        query = query.where(Ticket.column_id == column_id)
    if sprint_id:
        query = query.where(Ticket.sprint_id == sprint_id)
    if status:
        query = query.where(Ticket.status == status)
    
    query = query.offset(offset).limit(limit)
    query = query.order_by(Ticket.position)
    
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return [
        TicketResponseV2(
            id=str(ticket.id),
            title=ticket.title,
            description=ticket.description,
            priority=ticket.priority.value,
            status=ticket.status.value,
            position=ticket.position,
            dueDate=ticket.due_date,
            storyPoints=ticket.story_points,
            columnId=str(ticket.column_id),
            sprintId=str(ticket.sprint_id) if ticket.sprint_id else None,
            createdById=str(ticket.created_by_id),
            createdAt=ticket.created_at,
            updatedAt=ticket.updated_at
        )
        for ticket in tickets
    ]
