from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
import redis.asyncio as redis
from backend.app.core.config import settings

from backend.app.models.time_entry import TimeEntry, TimeEntryStatus
from backend.app.core.exceptions import NotFoundException, ValidationException


# Redis client for active timer
redis_client = redis.from_url(settings.REDIS_URL)


async def start_timer(db: AsyncSession, user_id: UUID, data: dict) -> TimeEntry:
    """Start a new time entry (timer)"""
    
    # Check if user already has a running timer
    active_key = f"active_timer:{user_id}"
    active = await redis_client.get(active_key)
    if active:
        raise ValidationException("You already have a running timer. Stop it first.")
    
    time_entry = TimeEntry(
        workspace_id=data.get("workspace_id"),  # You can pass this from context
        ticket_id=data.get("ticket_id"),
        user_id=user_id,
        started_at=datetime.utcnow(),
        description=data.get("description"),
        status=TimeEntryStatus.RUNNING
    )
    
    db.add(time_entry)
    await db.commit()
    await db.refresh(time_entry)
    
    # Store active timer in Redis
    await redis_client.setex(active_key, 86400, str(time_entry.id))  # 24h expiry
    
    return time_entry


async def stop_timer(db: AsyncSession, user_id: UUID, description: str = None) -> TimeEntry:
    """Stop the current running timer"""
    active_key = f"active_timer:{user_id}"
    entry_id = await redis_client.get(active_key)
    
    if not entry_id:
        raise NotFoundException("No active timer found")
    
    time_entry = await db.get(TimeEntry, entry_id)
    if not time_entry:
        await redis_client.delete(active_key)
        raise NotFoundException("Time entry not found")
    
    time_entry.stopped_at = datetime.utcnow()
    time_entry.duration_seconds = int((time_entry.stopped_at - time_entry.started_at).total_seconds())
    time_entry.status = TimeEntryStatus.LOGGED
    if description:
        time_entry.description = description
    
    await db.commit()
    await db.refresh(time_entry)
    
    # Remove active timer from Redis
    await redis_client.delete(active_key)
    
    return time_entry