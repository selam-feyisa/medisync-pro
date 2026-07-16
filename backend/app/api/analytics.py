from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
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
async def get_dashboard_summary(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardSummary:
    """Get dashboard summary metrics."""
    
    # Count tickets by status
    total_tickets_result = await db.execute(
        select(func.count(Ticket.id)).where(
            Ticket.column_id.in_(
                select(Ticket.column_id)
                .join(Ticket.column)
                .join(Ticket.column.board)
                .join(Ticket.column.board.project)
                .where(Ticket.column.board.project.workspace_id == workspace_id)
            )
        )
    )
    total_tickets = total_tickets_result.scalar() or 0
    
    open_tickets_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status == TicketStatus.TODO)
    )
    open_tickets = open_tickets_result.scalar() or 0
    
    in_progress_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status == TicketStatus.IN_PROGRESS)
    )
    in_progress_tickets = in_progress_result.scalar() or 0
    
    completed_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status == TicketStatus.DONE)
    )
    completed_tickets = completed_result.scalar() or 0
    
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
async def get_sprint_velocity(
    workspace_id: UUID,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[VelocityData]:
    """Get sprint velocity data for recent completed sprints."""
    from app.models.sprint import SprintStatus
    
    result = await db.execute(
        select(Sprint)
        .where(Sprint.status == SprintStatus.completed)
        .order_by(Sprint.created_at.desc())
        .limit(limit)
    )
    
    velocity_data = []
    for sprint in result.scalars():
        # Count completed tickets in this sprint
        completed_result = await db.execute(
            select(func.count(Ticket.id)).where(
                Ticket.sprint_id == sprint.id,
                Ticket.status == TicketStatus.DONE
            )
        )
        completed_tickets = completed_result.scalar() or 0
        
        # Sum story points
        points_result = await db.execute(
            select(func.sum(Ticket.story_points)).where(
                Ticket.sprint_id == sprint.id,
                Ticket.status == TicketStatus.DONE
            )
        )
        total_story_points = points_result.scalar() or 0.0
        
        velocity_data.append(VelocityData(
            sprint_name=sprint.name,
            completed_tickets=completed_tickets,
            total_story_points=total_story_points
        ))
    
    return velocity_data
