from fastapi import APIRouter

from app.services.boleto import get_boleto_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

boleto_router = APIRouter()


@boleto_router.get("/")
async def get_boleto(client: HttpxClientDep, cache_store: CacheDep):
    boleto_data = await cache_store.get_from_cache("boleto")
    if boleto_data is not None:
        return boleto_data

    boleto_data = await get_boleto_service(client)
    await cache_store.add_to_cache("boleto", boleto_data, ttl=86400)
    return boleto_data
