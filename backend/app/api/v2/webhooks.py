"""v2 Webhook API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.workspace_member import MemberRole
from app.models.webhook_subscription import WebhookSubscription
from app.models.webhook_delivery import WebhookDelivery
from app.services.webhook_service import get_webhook_service
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter(prefix="/webhooks", tags=["Webhooks v2"])


class WebhookSubscriptionCreate(BaseModel):
    """Request schema for creating webhook subscription."""
    targetUrl: str
    subscribedEvents: list[str]
    secret: str


class WebhookSubscriptionResponse(BaseModel):
    """Response schema for webhook subscription."""
    id: str
    workspaceId: str
    targetUrl: str
    subscribedEvents: list[str]
    isActive: bool
    createdAt: datetime
    updatedAt: datetime


class WebhookDeliveryResponse(BaseModel):
    """Response schema for webhook delivery."""
    id: str
    webhookId: str
    event: str
    responseStatus: Optional[int]
    retryCount: int
    success: bool
    deliveredAt: Optional[datetime]
    nextRetryAt: Optional[datetime]
    createdAt: datetime


@router.post("", response_model=WebhookSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_webhook_subscription(
    data: WebhookSubscriptionCreate,
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a webhook subscription."""
    webhook = WebhookSubscription(
        workspace_id=workspace_id,
        target_url=data.targetUrl,
        secret=data.secret,
        subscribed_events=json.dumps(data.subscribedEvents),
        is_active=True
    )
    
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    
    return WebhookSubscriptionResponse(
        id=str(webhook.id),
        workspaceId=str(webhook.workspace_id),
        targetUrl=webhook.target_url,
        subscribedEvents=json.loads(webhook.subscribed_events),
        isActive=webhook.is_active,
        createdAt=webhook.created_at,
        updatedAt=webhook.updated_at
    )


@router.get("", response_model=list[WebhookSubscriptionResponse])
async def list_webhook_subscriptions(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List webhook subscriptions for a workspace."""
    result = await db.execute(
        select(WebhookSubscription).where(
            WebhookSubscription.workspace_id == workspace_id
        )
    )
    webhooks = result.scalars().all()
    
    return [
        WebhookSubscriptionResponse(
            id=str(webhook.id),
            workspaceId=str(webhook.workspace_id),
            targetUrl=webhook.target_url,
            subscribedEvents=json.loads(webhook.subscribed_events),
            isActive=webhook.is_active,
            createdAt=webhook.created_at,
            updatedAt=webhook.updated_at
        )
        for webhook in webhooks
    ]


@router.get("/{webhook_id}/deliveries", response_model=list[WebhookDeliveryResponse])
async def list_webhook_deliveries(
    webhook_id: str,
    workspace_id: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List webhook deliveries for a subscription."""
    result = await db.execute(
        select(WebhookDelivery).where(
            WebhookDelivery.webhook_id == webhook_id
        ).order_by(WebhookDelivery.created_at.desc()).limit(limit)
    )
    deliveries = result.scalars().all()
    
    return [
        WebhookDeliveryResponse(
            id=str(delivery.id),
            webhookId=str(delivery.webhook_id),
            event=delivery.event,
            responseStatus=delivery.response_status,
            retryCount=delivery.retry_count,
            success=delivery.is_success,
            deliveredAt=delivery.delivered_at,
            nextRetryAt=delivery.next_retry_at,
            createdAt=delivery.created_at
        )
        for delivery in deliveries
    ]


@router.post("/{webhook_id}/retry")
async def retry_failed_deliveries(
    webhook_id: str,
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger retry of failed webhook deliveries."""
    webhook_service = get_webhook_service()
    await webhook_service.retry_failed_webhooks(db)
    
    return {"message": "Retry triggered for failed deliveries"}


@router.delete("/{webhook_id}")
async def delete_webhook_subscription(
    webhook_id: str,
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a webhook subscription."""
    result = await db.execute(
        select(WebhookSubscription).where(
            WebhookSubscription.id == webhook_id,
            WebhookSubscription.workspace_id == workspace_id
        )
    )
    webhook = result.scalar_one_or_none()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook subscription not found"
        )
    
    await db.delete(webhook)
    await db.commit()
    
    return {"message": "Webhook subscription deleted"}
