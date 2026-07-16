import json
import redis.asyncio as redis
from functools import wraps
from typing import Optional, Callable, Any
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cache(key: str) -> Optional[Any]:
    """Get value from Redis cache."""
    try:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception:
        return None


async def set_cache(key: str, value: Any, ttl: int = 300) -> bool:
    """Set value in Redis cache with TTL."""
    try:
        await redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception:
        return False


async def delete_cache(key: str) -> bool:
    """Delete key from Redis cache."""
    try:
        await redis_client.delete(key)
        return True
    except Exception:
        return False


async def delete_pattern(pattern: str) -> bool:
    """Delete keys matching pattern from Redis cache."""
    try:
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
        return True
    except Exception:
        return False


def cache_response(ttl: int = 300, key_prefix: str = ""):
    """Decorator to cache response in Redis."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = await get_cache(cache_key)
            if cached is not None:
                return cached
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            await set_cache(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
