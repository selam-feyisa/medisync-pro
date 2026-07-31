"""Billing service with Stripe integration."""

from typing import Optional
import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
from app.core.config import settings
from app.models.plan import Plan
from app.models.workspace_subscription import WorkspaceSubscription, SubscriptionStatus
from app.models.workspace_member import WorkspaceMember
from app.models.workspace import Workspace


class BillingService:
    """Service for billing operations with Stripe integration."""
    
    def __init__(self):
        if not settings.STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY not configured")
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    async def create_stripe_customer(
        self,
        email: str,
        name: str
    ) -> str:
        """Create a Stripe customer."""
        customer = stripe.Customer.create(
            email=email,
            name=name
        )
        return customer.id
    
    async def create_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str
    ) -> str:
        """Create a Stripe checkout session."""
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session.url
    
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str
    ) -> stripe.Subscription:
        """Create a Stripe subscription."""
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            expand=['latest_invoice.payment_intent']
        )
        return subscription
    
    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> stripe.Subscription:
        """Cancel a Stripe subscription."""
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=at_period_end
        )
        return subscription
    
    async def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Get a Stripe subscription."""
        return stripe.Subscription.retrieve(subscription_id)
    
    async def verify_seat_limit(
        self,
        workspace_id: str,
        db: AsyncSession
    ) -> tuple[bool, int, int]:
        """
        Verify if workspace is within seat limit.
        
        Returns:
            (is_within_limit, current_seats, seat_limit)
        """
        # Get workspace subscription
        result = await db.execute(
            select(WorkspaceSubscription).where(
                WorkspaceSubscription.workspace_id == workspace_id
            )
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            # No subscription, use free tier limit
            seat_limit = 5
        else:
            # Get plan seat limit
            result = await db.execute(
                select(Plan).where(Plan.id == subscription.plan_id)
            )
            plan = result.scalar_one_or_none()
            seat_limit = plan.seat_limit if plan else 5
        
        # Count current workspace members
        result = await db.execute(
            select(func.count(WorkspaceMember.id)).where(
                WorkspaceMember.workspace_id == workspace_id
            )
        )
        current_seats = result.scalar() or 0
        
        is_within_limit = current_seats < seat_limit
        
        return is_within_limit, current_seats, seat_limit
    
    async def handle_webhook_event(
        self,
        payload: bytes,
        sig_header: str,
        db: AsyncSession
    ) -> None:
        """
        Handle Stripe webhook events.
        
        Args:
            payload: Raw webhook payload
            sig_header: Stripe signature header
            db: Database session
        """
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise ValueError("STRIPE_WEBHOOK_SECRET not configured")
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            raise ValueError(f"Invalid payload: {str(e)}")
        except stripe.error.SignatureVerificationError as e:
            raise ValueError(f"Invalid signature: {str(e)}")
        
        # Handle different event types
        if event['type'] == 'checkout.session.completed':
            await self._handle_checkout_completed(event['data']['object'], db)
        elif event['type'] == 'customer.subscription.created':
            await self._handle_subscription_created(event['data']['object'], db)
        elif event['type'] == 'customer.subscription.updated':
            await self._handle_subscription_updated(event['data']['object'], db)
        elif event['type'] == 'customer.subscription.deleted':
            await self._handle_subscription_deleted(event['data']['object'], db)
        elif event['type'] == 'invoice.payment_succeeded':
            await self._handle_payment_succeeded(event['data']['object'], db)
        elif event['type'] == 'invoice.payment_failed':
            await self._handle_payment_failed(event['data']['object'], db)
    
    async def _handle_checkout_completed(self, session: dict, db: AsyncSession):
        """Handle checkout.session.completed event."""
        # Implementation depends on how you track workspace_id in metadata
        pass
    
    async def _handle_subscription_created(self, subscription: dict, db: AsyncSession):
        """Handle customer.subscription.created event."""
        # Find workspace by customer_id or metadata
        pass
    
    async def _handle_subscription_updated(self, subscription: dict, db: AsyncSession):
        """Handle customer.subscription.updated event."""
        # Update subscription status in database
        stripe_sub_id = subscription['id']
        result = await db.execute(
            select(WorkspaceSubscription).where(
                WorkspaceSubscription.stripe_subscription_id == stripe_sub_id
            )
        )
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            db_subscription.status = subscription['status']
            db_subscription.current_period_start = datetime.fromtimestamp(
                subscription['current_period_start']
            )
            db_subscription.current_period_end = datetime.fromtimestamp(
                subscription['current_period_end']
            )
            db_subscription.cancel_at_period_end = subscription.get('cancel_at_period_end', False)
            await db.commit()
    
    async def _handle_subscription_deleted(self, subscription: dict, db: AsyncSession):
        """Handle customer.subscription.deleted event."""
        stripe_sub_id = subscription['id']
        result = await db.execute(
            select(WorkspaceSubscription).where(
                WorkspaceSubscription.stripe_subscription_id == stripe_sub_id
            )
        )
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            db_subscription.status = SubscriptionStatus.canceled
            db_subscription.canceled_at = datetime.fromtimestamp(
                subscription.get('canceled_at', subscription[' canceled_at'])
            )
            await db.commit()
    
    async def _handle_payment_succeeded(self, invoice: dict, db: AsyncSession):
        """Handle invoice.payment_succeeded event."""
        # Update subscription to active if it was past_due
        pass
    
    async def _handle_payment_failed(self, invoice: dict, db: AsyncSession):
        """Handle invoice.payment_failed event."""
        # Update subscription to past_due
        stripe_sub_id = invoice['subscription']
        result = await db.execute(
            select(WorkspaceSubscription).where(
                WorkspaceSubscription.stripe_subscription_id == stripe_sub_id
            )
        )
        db_subscription = result.scalar_one_or_none()
        
        if db_subscription:
            db_subscription.status = SubscriptionStatus.past_due
            await db.commit()


def get_billing_service() -> Optional[BillingService]:
    """Get billing service instance if configured."""
    if settings.STRIPE_SECRET_KEY:
        return BillingService()
    return None
