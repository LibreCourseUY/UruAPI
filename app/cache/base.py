from abc import ABC, abstractmethod
from typing import Any


class CacheBackend(ABC):
    @abstractmethod
    async def get_from_cache(self, key: str) -> Any | None:
        """Return the cached value, or None if missing/expired."""

    @abstractmethod
    async def add_to_cache(self, key: str, value: Any, ttl: int) -> None:
        """Store value under key for `ttl` seconds."""

    @abstractmethod
    async def flush(self) -> None:
        """Remove all entries."""
