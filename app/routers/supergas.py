from fastapi import APIRouter

from app.services.supergas import get_supergas_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

supergas_router = APIRouter()

@supergas_router.get("/")
async def get_supergas(client :  HttpxClientDep, cache_store : CacheDep):
    supergas_value = await cache_store.get_from_cache("supergas")
    if supergas_value is not None:
        return {"supergas" : supergas_value}

    supergas_value = await get_supergas_service(client)
    await cache_store.add_to_cache("supergas", supergas_value, ttl=86400)
    return {"supergas" : supergas_value}
