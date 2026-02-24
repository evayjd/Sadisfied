from __future__ import annotations

import redis
from typing import Optional

from config import settings

_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    global _redis_client

    if _redis_client is not None:
        return _redis_client

    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,  
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
    )

    try:
        client.ping()
    except redis.RedisError as e:
        raise RuntimeError(f"Redis connection failed: {e}") from e

    _redis_client = client
    return _redis_client