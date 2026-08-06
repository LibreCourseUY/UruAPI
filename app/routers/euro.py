from fastapi import APIRouter

from app.services.euro import get_euro_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

euro_router = APIRouter()

@euro_router.get("/")
async def get_euro(client: HttpxClientDep, cache_store: CacheDep):
    euro_value = await cache_store.get_from_cache("euro")
    if euro_value is not None:
        return {"euro": euro_value}

    euro_value = await get_euro_service(client)
    await cache_store.add_to_cache("euro", euro_value, ttl=86400)
    return {"euro": euro_value}
