"""Webhook service with HMAC signing and retry logic."""

import hmac
import hashlib
import json
import httpx
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.webhook_subscription import WebhookSubscription
from app.models.webhook_delivery import WebhookDelivery
from app.core.config import settings
import asyncio


class WebhookService:
    """Service for delivering webhooks with HMAC signing and retries."""
    
    def __init__(self):
        self.max_retries = 5
        self.retry_delays = [60, 300, 900, 3600, 7200]  # 1min, 5min, 15min, 1hr, 2hr
    
    def generate_signature(self, payload: str, secret: str) -> str:
        """
        Generate HMAC SHA256 signature for webhook payload.
        
        Args:
            payload: JSON string payload
            secret: Webhook secret
            
        Returns:
            Hexadecimal signature string
        """
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def deliver_webhook(
        self,
        webhook_id: str,
        event: str,
        payload: dict,
        db: AsyncSession
    ) -> WebhookDelivery:
        """
        Deliver a webhook with retry logic.
        
        Args:
            webhook_id: ID of the webhook subscription
            event: Event type
            payload: Event payload
            db: Database session
            
        Returns:
            WebhookDelivery record
        """
        # Get webhook subscription
        result = await db.execute(
            select(WebhookSubscription).where(
                WebhookSubscription.id == webhook_id,
                WebhookSubscription.is_active == True
            )
        )
        webhook = result.scalar_one_or_none()
        
        if not webhook:
            raise ValueError("Webhook subscription not found or inactive")
        
        # Check if event is subscribed
        subscribed_events = json.loads(webhook.subscribed_events)
        if event not in subscribed_events:
            raise ValueError(f"Event {event} not subscribed")
        
        # Create delivery record
        payload_str = json.dumps(payload)
        delivery = WebhookDelivery(
            webhook_id=webhook_id,
            event=event,
            payload=payload_str,
            retry_count=0
        )
        db.add(delivery)
        await db.flush()
        
        # Attempt delivery
        await self._attempt_delivery(delivery, webhook, db)
        
        await db.commit()
        await db.refresh(delivery)
        
        return delivery
    
    async def _attempt_delivery(
        self,
        delivery: WebhookDelivery,
        webhook: WebhookSubscription,
        db: AsyncSession
    ):
        """
        Attempt to deliver webhook with signature.
        
        Args:
            delivery: WebhookDelivery record
            webhook: WebhookSubscription record
            db: Database session
        """
        payload_str = delivery.payload
        signature = self.generate_signature(payload_str, webhook.secret)
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Webhook-Event": delivery.event,
            "X-Webhook-ID": str(delivery.id)
        }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    webhook.target_url,
                    content=payload_str,
                    headers=headers
                )
                
                delivery.response_status = response.status_code
                delivery.response_body = response.text
                
                if response.status_code >= 200 and response.status_code < 300:
                    delivery.success = True
                    delivery.delivered_at = datetime.utcnow()
                else:
                    # Schedule retry if within max retries
                    if delivery.retry_count < self.max_retries:
                        delay = self.retry_delays[min(delivery.retry_count, len(self.retry_delays) - 1)]
                        delivery.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)
                        delivery.retry_count += 1
                    else:
                        # Max retries reached, mark as failed
                        delivery.success = False
        
        except Exception as e:
            delivery.response_status = 0
            delivery.response_body = str(e)
            
            # Schedule retry if within max retries
            if delivery.retry_count < self.max_retries:
                delay = self.retry_delays[min(delivery.retry_count, len(self.retry_delays) - 1)]
                delivery.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)
                delivery.retry_count += 1
            else:
                # Max retries reached, mark as failed
                delivery.success = False
    
    async def retry_failed_webhooks(self, db: AsyncSession):
        """
        Retry failed webhooks that are due for retry.
        
        Args:
            db: Database session
        """
        now = datetime.utcnow()
        
        result = await db.execute(
            select(WebhookDelivery).where(
                WebhookDelivery.success == False,
                WebhookDelivery.next_retry_at <= now,
                WebhookDelivery.retry_count < self.max_retries
            )
        )
        deliveries = result.scalars().all()
        
        for delivery in deliveries:
            # Get webhook subscription
            result = await db.execute(
                select(WebhookSubscription).where(
                    WebhookSubscription.id == delivery.webhook_id,
                    WebhookSubscription.is_active == True
                )
            )
            webhook = result.scalar_one_or_none()
            
            if webhook:
                await self._attempt_delivery(delivery, webhook, db)
        
        await db.commit()
    
    async def trigger_event(
        self,
        workspace_id: str,
        event: str,
        payload: dict,
        db: AsyncSession
    ):
        """
        Trigger an event to all subscribed webhooks for a workspace.
        
        Args:
            workspace_id: ID of the workspace
            event: Event type
            payload: Event payload
            db: Database session
        """
        # Get all active webhooks for the workspace
        result = await db.execute(
            select(WebhookSubscription).where(
                WebhookSubscription.workspace_id == workspace_id,
                WebhookSubscription.is_active == True
            )
        )
        webhooks = result.scalars().all()
        
        # Deliver to each webhook asynchronously
        tasks = []
        for webhook in webhooks:
            subscribed_events = json.loads(webhook.subscribed_events)
            if event in subscribed_events:
                tasks.append(self.deliver_webhook(str(webhook.id), event, payload, db))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


def get_webhook_service() -> WebhookService:
    """Get webhook service instance."""
    return WebhookService()
