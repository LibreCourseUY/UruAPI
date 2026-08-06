from fastapi import APIRouter

from app.services.pbi import get_pbi_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

pbi_router = APIRouter()

@pbi_router.get("/")
async def get_pbi(client: HttpxClientDep, cache_store: CacheDep):
    pbi_data = await cache_store.get_from_cache("pbi")
    if pbi_data is not None:
        return pbi_data

    pbi_data = await get_pbi_service(client)
    await cache_store.add_to_cache("pbi", pbi_data, ttl=86400)
    return pbi_data
