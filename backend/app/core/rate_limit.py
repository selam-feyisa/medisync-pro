import redis.asyncio as redis
from fastapi import HTTPException, Request
from functools import wraps
from typing import Callable
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def check_rate_limit(
    identifier: str,
    limit: int = 100,
    window: int = 60
) -> bool:
    """Check if identifier has exceeded rate limit."""
    key = f"rate_limit:{identifier}"
    
    current = await redis_client.incr(key)
    
    if current == 1:
        await redis_client.expire(key, window)
    
    return current <= limit


def rate_limit(limit: int = 100, window: int = 60, key_func: Callable = None):
    """Decorator to rate limit endpoints."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request from kwargs or args
            request = kwargs.get('request') or (args[0] if args else None)
            
            if not request:
                return await func(*args, **kwargs)
            
            # Generate identifier
            if key_func:
                identifier = key_func(request)
            else:
                identifier = request.client.host if request.client else "unknown"
            
            # Check rate limit
            allowed = await check_rate_limit(identifier, limit, window)
            
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Max {limit} requests per {window} seconds."
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


async def get_user_rate_limit_identifier(user_id: str) -> str:
    """Generate rate limit identifier for user."""
    return f"user:{user_id}"


async def get_ip_rate_limit_identifier(request: Request) -> str:
    """Generate rate limit identifier for IP address."""
    return f"ip:{request.client.host}" if request.client else "unknown"
