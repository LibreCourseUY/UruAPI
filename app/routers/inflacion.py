from fastapi import APIRouter

from app.services.inflacion import get_inflacion_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

inflacion_router = APIRouter()

@inflacion_router.get("/")
async def get_inflacion(client: HttpxClientDep, cache_store: CacheDep):
    inflacion_data = await cache_store.get_from_cache("inflacion")
    if inflacion_data is not None:
        return inflacion_data

    inflacion_data = await get_inflacion_service(client)
    await cache_store.add_to_cache("inflacion", inflacion_data, ttl=86400)
    return inflacion_data
