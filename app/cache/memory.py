import time
from typing import Any

from .base import CacheBackend
from .expiry import capped_ttl


class InMemoryCache(CacheBackend):
    """Dict-backed cache."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}

    async def get_from_cache(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.monotonic() >= expires_at:
            del self._store[key]
            return None
        return value

    async def add_to_cache(self, key: str, value: Any, ttl: int) -> None:
        self._store[key] = (value, time.monotonic() + capped_ttl(ttl))

    async def flush(self) -> None:
        self._store.clear()
