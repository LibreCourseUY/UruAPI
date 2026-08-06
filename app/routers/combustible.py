from fastapi import APIRouter

from app.services.combustible import get_combustible_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

combustible_router = APIRouter()

@combustible_router.get("/")
async def get_combustible(client: HttpxClientDep, cache_store: CacheDep):
    combustible_data = await cache_store.get_from_cache("combustible")
    if combustible_data is not None:
        return combustible_data

    combustible_data = await get_combustible_service(client)
    await cache_store.add_to_cache("combustible", combustible_data, ttl=86400)
    return combustible_data
