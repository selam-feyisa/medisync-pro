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