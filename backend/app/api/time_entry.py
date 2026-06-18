from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.time_entry import TimeEntryStart, TimeEntryResponse
from backend.app.services.time_entry import start_timer, stop_timer

router = APIRouter(prefix="/api/v1", tags=["Time Tracking"])


@router.post("/time-entries/start", response_model=TimeEntryResponse, status_code=status.HTTP_201_CREATED)
async def start_new_timer(
    data: TimeEntryStart,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a new time tracking timer"""
    entry = await start_timer(db, current_user.id, current_user.workspace_id if hasattr(current_user, 'workspace_id') else None, data.dict())
    return entry


@router.post("/time-entries/stop", response_model=TimeEntryResponse)
async def stop_current_timer(
    description: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Stop the currently running timer"""
    entry = await stop_timer(db, current_user.id, description)
    return entry

@router.post("/time-entries/manual", response_model=TimeEntryResponse)
async def create_manual_time_entry(
    data: TimeEntryManual,   # Use the schema we created
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create manual time entry for past logged hours"""
    entry = await create_manual_entry(db, current_user.id, current_user.workspace_id if hasattr(current_user, 'workspace_id') else None, data.dict())
    return entry