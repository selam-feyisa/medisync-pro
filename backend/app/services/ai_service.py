"""AI Service for OpenAI integration with quota tracking."""

from typing import Optional
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.ai_usage_log import AIUsageLog
from app.models.workspace_ai_quota import WorkspaceAIQuota
from app.models.user import User
from app.models.workspace import Workspace
from app.core.cache import cache_result
import redis.asyncio as aioredis


class AIService:
    """Service for AI operations with OpenAI integration."""
    
    # Token costs per 1K tokens (approximate USD)
    TOKEN_COSTS = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    }
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on token usage."""
        costs = self.TOKEN_COSTS.get(model, self.TOKEN_COSTS["gpt-3.5-turbo"])
        prompt_cost = (prompt_tokens / 1000) * costs["prompt"]
        completion_cost = (completion_tokens / 1000) * costs["completion"]
        return prompt_cost + completion_cost
    
    async def check_quota(
        self,
        workspace_id: str,
        db: AsyncSession
    ) -> WorkspaceAIQuota:
        """Check and update workspace AI quota."""
        result = await db.execute(
            select(WorkspaceAIQuota).where(
                WorkspaceAIQuota.workspace_id == workspace_id
            )
        )
        quota = result.scalar_one_or_none()
        
        # Create quota if it doesn't exist
        if not quota:
            quota = WorkspaceAIQuota(
                workspace_id=workspace_id,
                monthly_limit=100000,  # Default limit
                used_tokens=0,
                current_period_start=datetime.utcnow()
            )
            db.add(quota)
            await db.flush()
        
        # Reset quota if period has ended
        if quota.current_period_end and datetime.utcnow() > quota.current_period_end:
            quota.used_tokens = 0
            quota.current_period_start = datetime.utcnow()
            quota.current_period_end = None
        
        # Check if quota exceeded
        if quota.is_quota_exceeded:
            raise Exception("Monthly AI token quota exceeded")
        
        return quota
    
    async def log_usage(
        self,
        workspace_id: str,
        user_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cost: float,
        operation_type: str,
        model_used: str,
        db: AsyncSession
    ):
        """Log AI usage for tracking and billing."""
        usage_log = AIUsageLog(
            workspace_id=workspace_id,
            user_id=user_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            operation_type=operation_type,
            model_used=model_used
        )
        db.add(usage_log)
        
        # Update quota
        result = await db.execute(
            select(WorkspaceAIQuota).where(
                WorkspaceAIQuota.workspace_id == workspace_id
            )
        )
        quota = result.scalar_one_or_none()
        if quota:
            quota.used_tokens += total_tokens
    
    @cache_result(ttl=3600)  # Cache for 1 hour
    async def summarize_ticket(
        self,
        ticket_id: str,
        include_comments: bool,
        workspace_id: str,
        user_id: str,
        db: AsyncSession
    ) -> dict:
        """Generate a summary for a ticket."""
        # In a real implementation, fetch ticket data from database
        ticket_content = f"Ticket {ticket_id} content here"
        
        if include_comments:
            ticket_content += " with comments"
        
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes tickets concisely."
                },
                {
                    "role": "user",
                    "content": f"Summarize this ticket: {ticket_content}"
                }
            ]
        )
        
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        cost = self.calculate_cost("gpt-3.5-turbo", prompt_tokens, completion_tokens)
        
        # Log usage
        await self.log_usage(
            workspace_id=workspace_id,
            user_id=user_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            operation_type="ticket_summarize",
            model_used="gpt-3.5-turbo",
            db=db
        )
        
        return {
            "result": response.choices[0].message.content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": cost,
            "model_used": "gpt-3.5-turbo"
        }
    
    async def generate_pr_description(
        self,
        workspace_id: str,
        context: str,
        user_id: str,
        db: AsyncSession
    ) -> dict:
        """Generate a PR/workspace description."""
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that writes clear PR descriptions."
                },
                {
                    "role": "user",
                    "content": f"Write a PR description for this workspace with context: {context}"
                }
            ]
        )
        
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        cost = self.calculate_cost("gpt-3.5-turbo", prompt_tokens, completion_tokens)
        
        # Log usage
        await self.log_usage(
            workspace_id=workspace_id,
            user_id=user_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            operation_type="pr_description",
            model_used="gpt-3.5-turbo",
            db=db
        )
        
        return {
            "result": response.choices[0].message.content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": cost,
            "model_used": "gpt-3.5-turbo"
        }


def get_ai_service() -> Optional[AIService]:
    """Get AI service instance if configured."""
    if settings.OPENAI_API_KEY:
        return AIService()
    return None
