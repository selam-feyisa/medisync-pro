"""Admin API endpoints for system administration."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import require_superadmin
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.feature_flag import FeatureFlag
from app.core.config import settings
import redis.asyncio as aioredis
import stripe

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/workspaces/audit-log")
async def get_audit_log(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    action_type: Optional[str] = None,
    actor_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Get audit log with optional filters."""
    query = select(AuditLog)
    
    # Apply filters
    if start_date:
        query = query.where(AuditLog.created_at >= start_date)
    if end_date:
        query = query.where(AuditLog.created_at <= end_date)
    if action_type:
        query = query.where(AuditLog.action_type == action_type)
    if actor_id:
        query = query.where(AuditLog.actor_id == actor_id)
    
    # Order by created_at descending
    query = query.order_by(AuditLog.created_at.desc())
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    audit_logs = result.scalars().all()
    
    return [
        {
            "id": str(log.id),
            "actor_id": str(log.actor_id),
            "action_type": log.action_type,
            "entity_type": log.entity_type,
            "entity_id": str(log.entity_id),
            "old_values": log.old_values,
            "new_values": log.new_values,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at.isoformat() if log.created_at else None
        }
        for log in audit_logs
    ]


@router.get("/feature-flags")
async def list_feature_flags(
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """List all feature flags."""
    result = await db.execute(select(FeatureFlag))
    flags = result.scalars().all()
    
    return [
        {
            "id": str(flag.id),
            "key": flag.key,
            "is_enabled": flag.is_enabled,
            "description": flag.description,
            "created_at": flag.created_at.isoformat() if flag.created_at else None,
            "updated_at": flag.updated_at.isoformat() if flag.updated_at else None
        }
        for flag in flags
    ]


@router.post("/feature-flags")
async def create_feature_flag(
    key: str,
    is_enabled: bool = False,
    description: Optional[str] = None,
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Create a new feature flag."""
    # Check if key already exists
    result = await db.execute(select(FeatureFlag).where(FeatureFlag.key == key))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feature flag with this key already exists"
        )
    
    flag = FeatureFlag(
        key=key,
        is_enabled=is_enabled,
        description=description
    )
    db.add(flag)
    await db.commit()
    await db.refresh(flag)
    
    return {
        "id": str(flag.id),
        "key": flag.key,
        "is_enabled": flag.is_enabled,
        "description": flag.description,
        "created_at": flag.created_at.isoformat() if flag.created_at else None,
        "updated_at": flag.updated_at.isoformat() if flag.updated_at else None
    }


@router.patch("/feature-flags/{flag_id}")
async def update_feature_flag(
    flag_id: str,
    is_enabled: Optional[bool] = None,
    description: Optional[str] = None,
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Update a feature flag."""
    result = await db.execute(select(FeatureFlag).where(FeatureFlag.id == flag_id))
    flag = result.scalar_one_or_none()
    
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature flag not found"
        )
    
    if is_enabled is not None:
        flag.is_enabled = is_enabled
    if description is not None:
        flag.description = description
    
    await db.commit()
    await db.refresh(flag)
    
    return {
        "id": str(flag.id),
        "key": flag.key,
        "is_enabled": flag.is_enabled,
        "description": flag.description,
        "created_at": flag.created_at.isoformat() if flag.created_at else None,
        "updated_at": flag.updated_at.isoformat() if flag.updated_at else None
    }


@router.delete("/feature-flags/{flag_id}")
async def delete_feature_flag(
    flag_id: str,
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Delete a feature flag."""
    result = await db.execute(select(FeatureFlag).where(FeatureFlag.id == flag_id))
    flag = result.scalar_one_or_none()
    
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature flag not found"
        )
    
    await db.delete(flag)
    await db.commit()
    
    return {"message": "Feature flag deleted successfully"}


@router.get("/health/detailed")
async def detailed_health_check(
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Detailed health check for all system components."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check PostgreSQL
    try:
        await db.execute(select(1))
        health_status["components"]["postgresql"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["components"]["postgresql"] = {
            "status": "unhealthy",
            "message": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        health_status["components"]["redis"] = {
            "status": "healthy",
            "message": "Redis connection successful"
        }
    except Exception as e:
        health_status["components"]["redis"] = {
            "status": "unhealthy",
            "message": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check Stripe (if configured)
    if settings.STRIPE_SECRET_KEY:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # Simple API call to check connectivity
            stripe.Plan.list(limit=1)
            health_status["components"]["stripe"] = {
                "status": "healthy",
                "message": "Stripe API connection successful"
            }
        except Exception as e:
            health_status["components"]["stripe"] = {
                "status": "unhealthy",
                "message": str(e)
            }
            health_status["status"] = "degraded"
    else:
        health_status["components"]["stripe"] = {
            "status": "not_configured",
            "message": "Stripe not configured"
        }
    
    # Check OpenAI (if configured)
    if settings.OPENAI_API_KEY:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            # Simple API call to check connectivity
            await client.models.list()
            health_status["components"]["openai"] = {
                "status": "healthy",
                "message": "OpenAI API connection successful"
            }
        except Exception as e:
            health_status["components"]["openai"] = {
                "status": "unhealthy",
                "message": str(e)
            }
            health_status["status"] = "degraded"
    else:
        health_status["components"]["openai"] = {
            "status": "not_configured",
            "message": "OpenAI not configured"
        }
    
    # Check MinIO (if configured)
    if settings.MINIO_URL:
        try:
            from minio import Minio
            client = Minio(
                settings.MINIO_URL,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False
            )
            client.list_buckets()
            health_status["components"]["minio"] = {
                "status": "healthy",
                "message": "MinIO connection successful"
            }
        except Exception as e:
            health_status["components"]["minio"] = {
                "status": "unhealthy",
                "message": str(e)
            }
            health_status["status"] = "degraded"
    else:
        health_status["components"]["minio"] = {
            "status": "not_configured",
            "message": "MinIO not configured"
        }
    
    return health_status


@router.get("/stats")
async def get_admin_stats(
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Get administrative statistics."""
    from app.models.user import User
    from app.models.workspace import Workspace
    from app.models.ticket import Ticket
    from sqlalchemy import func
    
    stats = {}
    
    # User stats
    result = await db.execute(select(func.count(User.id)))
    stats["total_users"] = result.scalar() or 0
    
    result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    stats["active_users"] = result.scalar() or 0
    
    # Workspace stats
    result = await db.execute(select(func.count(Workspace.id)))
    stats["total_workspaces"] = result.scalar() or 0
    
    # Ticket stats
    result = await db.execute(select(func.count(Ticket.id)))
    stats["total_tickets"] = result.scalar() or 0
    
    return stats
