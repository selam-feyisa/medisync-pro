from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timedelta
import redis.asyncio as redis

from backend.app.core.config import settings
from backend.app.models.time_entry import TimeEntry, TimeEntryStatus
from backend.app.core.exceptions import NotFoundException, ValidationException


redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def start_timer(db: AsyncSession, user_id: UUID, workspace_id: UUID, data: dict):
    """Start a new time entry"""
    active_key = f"active_timer:{user_id}"
    if await redis_client.exists(active_key):
        raise ValidationException("You already have a running timer. Please stop it first.")

    time_entry = TimeEntry(
        workspace_id=workspace_id,
        ticket_id=data.get("ticket_id"),
        user_id=user_id,
        started_at=datetime.utcnow(),
        description=data.get("description"),
        is_billable=data.get("is_billable", True),
        status=TimeEntryStatus.RUNNING
    )

    db.add(time_entry)
    await db.commit()
    await db.refresh(time_entry)

    await redis_client.setex(active_key, 86400, str(time_entry.id))  # 24 hours
    return time_entry


async def stop_timer(db: AsyncSession, user_id: UUID, description: str = None):
    """Stop current running timer"""
    active_key = f"active_timer:{user_id}"
    entry_id_str = await redis_client.get(active_key)

async def create_manual_entry(db: AsyncSession, user_id: UUID, workspace_id: UUID, data: dict):
    """Create manual time entry for past work"""
    if data["stopped_at"] <= data["started_at"]:
        raise ValidationException("Stopped time must be after started time")
    
    duration = int((data["stopped_at"] - data["started_at"]).total_seconds())
    if duration > 86400:  # 24 hours
        raise ValidationException("Duration cannot exceed 24 hours")

    time_entry = TimeEntry(
        workspace_id=workspace_id,
        ticket_id=data.get("ticket_id"),
        user_id=user_id,
        started_at=data["started_at"],
        stopped_at=data["stopped_at"],
        duration_seconds=duration,
        description=data.get("description"),
        is_billable=data.get("is_billable", True),
        status=TimeEntryStatus.LOGGED
    )

    db.add(time_entry)
    await db.commit()
    await db.refresh(time_entry)
    return time_entry

    if not entry_id_str:
        raise NotFoundException("No active timer found for this user.")

    time_entry = await db.get(TimeEntry, UUID(entry_id_str))
    if not time_entry:
        await redis_client.delete(active_key)
        raise NotFoundException("Time entry record not found.")

    time_entry.stopped_at = datetime.utcnow()
    time_entry.duration_seconds = int((time_entry.stopped_at - time_entry.started_at).total_seconds())
    time_entry.status = TimeEntryStatus.LOGGED
    if description:
        time_entry.description = description

    await db.commit()
    await db.refresh(time_entry)
    await redis_client.delete(active_key)

    return time_entry
async def submit_time_entry(db: AsyncSession, entry_id: UUID, user_id: UUID):
    """Submit time entry for approval"""
    entry = await db.get(TimeEntry, entry_id)
    if not entry or entry.user_id != user_id:
        raise NotFoundException("Time entry not found")
    
    if entry.status != TimeEntryStatus.LOGGED:
        raise ValidationException("Only logged entries can be submitted")
    
    entry.status = TimeEntryStatus.SUBMITTED
    await db.commit()
    await db.refresh(entry)
    return entry


async def approve_time_entry(db: AsyncSession, entry_id: UUID):
    """Approve time entry (admin/manager only - role check in API later)"""
    entry = await db.get(TimeEntry, entry_id)
    if not entry:
        raise NotFoundException("Time entry not found")
    
    entry.status = TimeEntryStatus.APPROVED
    await db.commit()
    await db.refresh(entry)
    return entry
async def get_weekly_summary(db: AsyncSession, user_id: UUID):
    """Get weekly time summary for current user"""
    # Simple implementation - expand with proper date filtering later
    result = await db.execute(
        select(TimeEntry).where(TimeEntry.user_id == user_id)
    )
    entries = result.scalars().all()
    
    total_seconds = sum(e.duration_seconds or 0 for e in entries if e.duration_seconds)
    
    return {
        "total_hours": round(total_seconds / 3600, 2),
        "entries_count": len(entries),
        "message": "Weekly summary ready (expand with date range later)"
    }