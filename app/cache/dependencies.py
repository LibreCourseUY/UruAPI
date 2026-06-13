from typing import Annotated
from fastapi import Depends

from app.config import settings

from .base import CacheBackend
from .memory import InMemoryCache
from .redis import RedisCache


def build_cache() -> CacheBackend:
    if settings.cache_backend == "redis":
        return RedisCache(settings.redis_url)
    return InMemoryCache()


cache: CacheBackend = build_cache()


async def get_cache() -> CacheBackend:
    return cache


CacheDep = Annotated[CacheBackend, Depends(get_cache)]
