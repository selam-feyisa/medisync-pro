"""Billing API endpoints for subscription management."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.workspace import Workspace
from app.models.plan import Plan
from app.models.workspace_subscription import WorkspaceSubscription, SubscriptionStatus
from app.services.billing_service import get_billing_service
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/billing", tags=["Billing"])


class CreateSubscriptionRequest(BaseModel):
    """Request schema for creating a subscription."""
    workspace_id: str
    plan_id: str


class SubscriptionResponse(BaseModel):
    """Response schema for subscription details."""
    id: str
    workspace_id: str
    plan_id: str
    status: str
    current_period_start: Optional[str]
    current_period_end: Optional[str]
    cancel_at_period_end: bool
    is_active: bool
    is_trialing: bool


class SeatLimitResponse(BaseModel):
    """Response schema for seat limit check."""
    is_within_limit: bool
    current_seats: int
    seat_limit: int
    can_add_member: bool


@router.post("/workspaces/{workspace_id}/subscription", response_model=SubscriptionResponse)
async def create_subscription(
    workspace_id: str,
    request: CreateSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a subscription for a workspace."""
    billing_service = get_billing_service()
    if not billing_service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Billing service not configured"
        )
    
    # Check if user is workspace owner
    result = await db.execute(
        select(Workspace).where(
            Workspace.id == workspace_id,
            Workspace.owner_id == str(current_user.id)
        )
    )
    workspace = result.scalar_one_or_none()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owners can create subscriptions"
        )
    
    # Check if subscription already exists
    result = await db.execute(
        select(WorkspaceSubscription).where(
            WorkspaceSubscription.workspace_id == workspace_id
        )
    )
    existing_subscription = result.scalar_one_or_none()
    
    if existing_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription already exists for this workspace"
        )
    
    # Get plan
    result = await db.execute(
        select(Plan).where(Plan.id == request.plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    
    # Create Stripe customer if needed
    stripe_customer_id = await billing_service.create_stripe_customer(
        email=current_user.email,
        name=current_user.full_name
    )
    
    # Create checkout session
    success_url = f"{current_user.email}/billing/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{current_user.email}/billing/cancel"
    
    checkout_url = await billing_service.create_checkout_session(
        customer_id=stripe_customer_id,
        price_id=plan.stripe_price_id,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    # Create subscription record (in trialing state)
    subscription = WorkspaceSubscription(
        workspace_id=workspace_id,
        plan_id=request.plan_id,
        stripe_customer_id=stripe_customer_id,
        status=SubscriptionStatus.trialing
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    
    return {
        "checkout_url": checkout_url,
        "subscription": SubscriptionResponse(
            id=str(subscription.id),
            workspace_id=str(subscription.workspace_id),
            plan_id=str(subscription.plan_id),
            status=subscription.status.value,
            current_period_start=subscription.current_period_start.isoformat() if subscription.current_period_start else None,
            current_period_end=subscription.current_period_end.isoformat() if subscription.current_period_end else None,
            cancel_at_period_end=subscription.cancel_at_period_end,
            is_active=subscription.is_active,
            is_trialing=subscription.is_trialing
        )
    }


@router.get("/workspaces/{workspace_id}/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get subscription details for a workspace."""
    result = await db.execute(
        select(WorkspaceSubscription).where(
            WorkspaceSubscription.workspace_id == workspace_id
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    return SubscriptionResponse(
        id=str(subscription.id),
        workspace_id=str(subscription.workspace_id),
        plan_id=str(subscription.plan_id),
        status=subscription.status.value,
        current_period_start=subscription.current_period_start.isoformat() if subscription.current_period_start else None,
        current_period_end=subscription.current_period_end.isoformat() if subscription.current_period_end else None,
        cancel_at_period_end=subscription.cancel_at_period_end,
        is_active=subscription.is_active,
        is_trialing=subscription.is_trialing
    )


@router.post("/workspaces/{workspace_id}/subscription/cancel")
async def cancel_subscription(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a workspace subscription."""
    billing_service = get_billing_service()
    if not billing_service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Billing service not configured"
        )
    
    # Check if user is workspace owner
    result = await db.execute(
        select(Workspace).where(
            Workspace.id == workspace_id,
            Workspace.owner_id == str(current_user.id)
        )
    )
    workspace = result.scalar_one_or_none()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owners can cancel subscriptions"
        )
    
    # Get subscription
    result = await db.execute(
        select(WorkspaceSubscription).where(
            WorkspaceSubscription.workspace_id == workspace_id
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Cancel in Stripe
    if subscription.stripe_subscription_id:
        await billing_service.cancel_subscription(
            subscription.stripe_subscription_id,
            at_period_end=True
        )
    
    # Update database
    subscription.cancel_at_period_end = True
    await db.commit()
    
    return {"message": "Subscription scheduled for cancellation"}


@router.get("/workspaces/{workspace_id}/seat-limit", response_model=SeatLimitResponse)
async def check_seat_limit(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check if workspace is within seat limit."""
    billing_service = get_billing_service()
    
    if billing_service:
        is_within_limit, current_seats, seat_limit = await billing_service.verify_seat_limit(
            workspace_id, db
        )
    else:
        # Default to free tier if billing not configured
        from sqlalchemy import func
        from app.models.workspace_member import WorkspaceMember
        
        result = await db.execute(
            select(func.count(WorkspaceMember.id)).where(
                WorkspaceMember.workspace_id == workspace_id
            )
        )
        current_seats = result.scalar() or 0
        seat_limit = 5
        is_within_limit = current_seats < seat_limit
    
    return SeatLimitResponse(
        is_within_limit=is_within_limit,
        current_seats=current_seats,
        seat_limit=seat_limit,
        can_add_member=is_within_limit
    )


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Stripe webhook events."""
    billing_service = get_billing_service()
    if not billing_service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Billing service not configured"
        )
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )
    
    try:
        await billing_service.handle_webhook_event(payload, sig_header, db)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {str(e)}"
        )


@router.get("/plans")
async def list_plans(db: AsyncSession = Depends(get_db)):
    """List available subscription plans."""
    result = await db.execute(
        select(Plan).where(Plan.is_active == True, Plan.is_public == True)
    )
    plans = result.scalars().all()
    
    return [
        {
            "id": str(plan.id),
            "name": plan.name,
            "plan_type": plan.plan_type,
            "price": plan.price,
            "currency": plan.currency,
            "interval": plan.interval,
            "seat_limit": plan.seat_limit,
            "ai_tokens_limit": plan.ai_tokens_limit,
            "features": plan.features
        }
        for plan in plans
    ]
