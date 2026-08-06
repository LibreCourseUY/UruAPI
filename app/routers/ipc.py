from fastapi import APIRouter

from app.services.ipc import get_ipc_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

ipc_router = APIRouter()

@ipc_router.get("/")
async def get_ipc(client: HttpxClientDep, cache_store: CacheDep):
    ipc_data = await cache_store.get_from_cache("ipc")
    if ipc_data is not None:
        return ipc_data

    ipc_data = await get_ipc_service(client)
    await cache_store.add_to_cache("ipc", ipc_data, ttl=86400)
    return ipc_data
