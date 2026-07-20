from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from uuid import UUID
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.cache import cache_response
from app.models import User, Ticket, TimeEntry, Sprint
from app.models.ticket import TicketStatus

router = APIRouter(prefix="/analytics", tags=["analytics"])


class DashboardSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    completed_tickets: int
    in_progress_tickets: int
    total_time_logged: float  # hours
    active_sprints: int
    recent_activity_count: int


class TicketDistribution(BaseModel):
    by_status: dict
    by_priority: dict
    by_assignee: dict


class VelocityData(BaseModel):
    sprint_name: str
    completed_tickets: int
    total_story_points: float


@router.get("/dashboard/summary", response_model=DashboardSummary)
@cache_response(ttl=60, key_prefix="analytics")
async def get_dashboard_summary(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardSummary:
    """Get dashboard summary metrics."""
    
    # Optimize: Combine ticket status counts into single query
    ticket_counts_result = await db.execute(
        select(
            Ticket.status,
            func.count(Ticket.id)
        ).where(
            Ticket.column_id.in_(
                select(Ticket.column_id)
                .join(Ticket.column)
                .join(Ticket.column.board)
                .join(Ticket.column.board.project)
                .where(Ticket.column.board.project.workspace_id == workspace_id)
            )
        ).group_by(Ticket.status)
    )
    
    ticket_counts = {str(status): count for status, count in ticket_counts_result.all()}
    total_tickets = sum(ticket_counts.values())
    open_tickets = ticket_counts.get(str(TicketStatus.TODO), 0)
    in_progress_tickets = ticket_counts.get(str(TicketStatus.IN_PROGRESS), 0)
    completed_tickets = ticket_counts.get(str(TicketStatus.DONE), 0)
    
    # Total time logged
    time_result = await db.execute(
        select(func.sum(TimeEntry.duration_seconds)).where(
            TimeEntry.workspace_id == workspace_id
        )
    )
    total_seconds = time_result.scalar() or 0
    total_time_logged = round(total_seconds / 3600, 2)
    
    # Active sprints
    from app.models.sprint import SprintStatus
    sprint_result = await db.execute(
        select(func.count(Sprint.id)).where(
            Sprint.status == SprintStatus.active
        )
    )
    active_sprints = sprint_result.scalar() or 0
    
    # Recent activity (last 7 days)
    from app.models.ticket_activity import TicketActivity
    week_ago = datetime.utcnow() - timedelta(days=7)
    activity_result = await db.execute(
        select(func.count(TicketActivity.id)).where(
            TicketActivity.created_at >= week_ago
        )
    )
    recent_activity_count = activity_result.scalar() or 0
    
    return DashboardSummary(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        completed_tickets=completed_tickets,
        in_progress_tickets=in_progress_tickets,
        total_time_logged=total_time_logged,
        active_sprints=active_sprints,
        recent_activity_count=recent_activity_count
    )


@router.get("/tickets/distribution", response_model=TicketDistribution)
async def get_ticket_distribution(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TicketDistribution:
    """Get ticket distribution by status, priority, and assignee."""
    
    # By status
    status_result = await db.execute(
        select(Ticket.status, func.count(Ticket.id))
        .group_by(Ticket.status)
    )
    by_status = {str(status): count for status, count in status_result.all()}
    
    # By priority
    priority_result = await db.execute(
        select(Ticket.priority, func.count(Ticket.id))
        .group_by(Ticket.priority)
    )
    by_priority = {str(priority): count for priority, count in priority_result.all()}
    
    # By assignee (simplified)
    by_assignee = {"unassigned": 0}  # Placeholder for assignee distribution
    
    return TicketDistribution(
        by_status=by_status,
        by_priority=by_priority,
        by_assignee=by_assignee
    )


@router.get("/sprints/velocity", response_model=List[VelocityData])
@cache_response(ttl=300, key_prefix="analytics")
async def get_sprint_velocity(
    workspace_id: UUID,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[VelocityData]:
    """Get sprint velocity data for recent completed sprints."""
    from app.models.sprint import SprintStatus
    
    # Optimize: Use single query with joins to get sprint and ticket data
    result = await db.execute(
        select(
            Sprint.id,
            Sprint.name,
            func.count(Ticket.id).label('completed_count'),
            func.sum(Ticket.story_points).label('total_points')
        )
        .outerjoin(Ticket, (Ticket.sprint_id == Sprint.id) & (Ticket.status == TicketStatus.DONE))
        .where(Sprint.status == SprintStatus.completed)
        .group_by(Sprint.id, Sprint.name)
        .order_by(Sprint.created_at.desc())
        .limit(limit)
    )
    
    velocity_data = []
    for row in result:
        velocity_data.append(VelocityData(
            sprint_name=row.name,
            completed_tickets=row.completed_count or 0,
            total_story_points=row.total_points or 0.0
        ))
    
    return velocity_data
