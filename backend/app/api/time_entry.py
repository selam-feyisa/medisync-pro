from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.time_entry import TimeEntryStart, TimeEntryResponse, TimeEntryManual
from backend.app.services.time_entry import (
    start_timer, 
    stop_timer, 
    create_manual_entry, 
    submit_time_entry, 
    approve_time_entry,
    get_weekly_summary   # New import
)

router = APIRouter(prefix="/api/v1", tags=["Time Tracking"])


@router.post("/time-entries/start", response_model=TimeEntryResponse, status_code=status.HTTP_201_CREATED)
async def start_new_timer(
    data: TimeEntryStart,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a new time tracking timer"""
    entry = await start_timer(db, current_user.id, getattr(current_user, 'workspace_id', None), data.dict())
    return entry


@router.post("/time-entries/stop", response_model=TimeEntryResponse)
async def stop_current_timer(
    description: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Stop the currently running timer"""
    entry = await stop_timer(db, current_user.id, description)
    return entry


@router.post("/time-entries/manual", response_model=TimeEntryResponse)
async def create_manual_time_entry(
    data: TimeEntryManual,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create manual time entry for past work"""
    entry = await create_manual_entry(db, current_user.id, getattr(current_user, 'workspace_id', None), data.dict())
    return entry


@router.post("/time-entries/{entry_id}/submit", response_model=TimeEntryResponse)
async def submit_for_approval(
    entry_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit time entry for manager approval"""
    entry = await submit_time_entry(db, entry_id, current_user.id)
    return entry


@router.post("/time-entries/{entry_id}/approve", response_model=TimeEntryResponse)
async def approve_time_entry_endpoint(
    entry_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve a submitted time entry (admin/manager only)"""
    entry = await approve_time_entry(db, entry_id)
    return entry


# New Weekly Report Endpoint
@router.get("/users/me/time-entries/weekly", response_model=dict)
async def get_my_weekly_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's weekly time tracking summary"""
    summary = await get_weekly_summary(db, current_user.id)
    return summary