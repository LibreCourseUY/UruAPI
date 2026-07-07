from fastapi import APIRouter

from app.services.real import get_real_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

real_router = APIRouter()

@real_router.get("/")
async def get_real(client: HttpxClientDep, cache_store: CacheDep):
    real_value = await cache_store.get_from_cache("real")
    if real_value is not None:
        return {"real": real_value}
    
    real_value = await get_real_service(client)
    await cache_store.add_to_cache("real", real_value, ttl=86400)
    return {"real": real_value}