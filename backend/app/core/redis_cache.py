"""
ContentIQ - Redis Caching Utility
Provides caching with TTL for heavy analytical and intelligence endpoints.
Features graceful fallback: If Redis is unavailable or disconnected, it bypasses
the cache without interrupting API execution.
"""
import json
import logging
from typing import Optional, Any
import redis
from app.core.config import settings

logger = logging.getLogger("contentiq.cache")

# Global Redis client instance with connection pooling
_redis_client: Optional[redis.Redis] = None

def get_redis_client() -> Optional[redis.Redis]:
    """Retrieves or initializes the Redis client instance."""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=1.5,
                socket_connect_timeout=1.5
            )
            # Ping to verify active connection
            _redis_client.ping()
        except Exception as e:
            logger.warning(f"[ContentIQ Redis] Unable to connect to Redis ({e}). Gracefully falling back to uncached execution.")
            _redis_client = None
    return _redis_client

def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve cached data by key.
    Returns deserialized JSON object if found, else None.
    """
    try:
        client = get_redis_client()
        if client is None:
            return None
        cached_val = client.get(key)
        if cached_val:
            return json.loads(cached_val)
    except Exception as e:
        logger.debug(f"[ContentIQ Redis] Cache get failed for {key}: {e}")
    return None

def set_cache(key: str, value: Any, ttl_seconds: int = 60) -> bool:
    """
    Store JSON-serializable data into Redis cache with a short TTL (default 60s).
    Returns True if successfully stored, False otherwise.
    """
    try:
        client = get_redis_client()
        if client is None:
            return False
        serialized = json.dumps(value, default=str)
        client.setex(key, ttl_seconds, serialized)
        return True
    except Exception as e:
        logger.debug(f"[ContentIQ Redis] Cache set failed for {key}: {e}")
        return False

def delete_cache(key: str) -> bool:
    """Evict a specific cache key."""
    try:
        client = get_redis_client()
        if client is None:
            return False
        client.delete(key)
        return True
    except Exception as e:
        logger.debug(f"[ContentIQ Redis] Cache delete failed for {key}: {e}")
        return False

def clear_tenant_cache(tenant_id: str) -> bool:
    """Invalidate all cached keys for a specific tenant."""
    try:
        client = get_redis_client()
        if client is None:
            return False
        keys = client.keys(f"*{tenant_id}*")
        if keys:
            client.delete(*keys)
        return True
    except Exception as e:
        logger.debug(f"[ContentIQ Redis] Tenant cache clear failed for {tenant_id}: {e}")
        return False
