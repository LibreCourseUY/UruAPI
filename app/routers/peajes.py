from fastapi import APIRouter

from app.services.peajes import get_peajes_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

peajes_router = APIRouter()

@peajes_router.get("/")
async def get_peajes(client: HttpxClientDep, cache_store: CacheDep):
    peajes_data = await cache_store.get_from_cache("peajes")
    if peajes_data is not None:
        return peajes_data

    peajes_data = await get_peajes_service(client)
    await cache_store.add_to_cache("peajes", peajes_data, ttl=86400)
    return peajes_data
