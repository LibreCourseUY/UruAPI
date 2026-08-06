from fastapi import APIRouter

from app.services.ur import get_ur_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

ur_router = APIRouter()

@ur_router.get("/")
async def get_ur(client: HttpxClientDep, cache_store: CacheDep):
    ur_value = await cache_store.get_from_cache("ur")
    if ur_value is not None:
        return {"ur": ur_value}

    ur_value = await get_ur_service(client)
    await cache_store.add_to_cache("ur", ur_value, ttl=86400)
    return {"ur": ur_value}
