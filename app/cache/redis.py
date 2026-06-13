import json
from typing import Any

from redis.asyncio import Redis

from .base import CacheBackend
from .expiry import capped_ttl


class RedisCache(CacheBackend):
    """Redis-backed cache."""

    def __init__(self, redis_url: str) -> None:
        self._client: Redis = Redis.from_url(redis_url, decode_responses=True)

    async def get_from_cache(self, key: str) -> Any | None:
        raw = await self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def add_to_cache(self, key: str, value: Any, ttl: int) -> None:
        ex = max(1, int(capped_ttl(ttl)))
        await self._client.set(key, json.dumps(value), ex=ex)

    async def flush(self) -> None:
        await self._client.flushdb()
