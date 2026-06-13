from fastapi import APIRouter

from app.services.dolar import get_dolar_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

dolar_router = APIRouter()

@dolar_router.get("/")
async def get_dolar(client :  HttpxClientDep, cache_store : CacheDep):
    dolar_value = await cache_store.get_from_cache("dolar")
    if dolar_value is not None:
        return {"dolar" : dolar_value}
    
    dolar_value = await get_dolar_service(client)
    await cache_store.add_to_cache("dolar", dolar_value, ttl=86400)
    return {"dolar" : dolar_value}