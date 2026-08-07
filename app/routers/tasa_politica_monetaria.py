from fastapi import APIRouter

from app.services.tasa_politica_monetaria import get_tasa_politica_monetaria_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

tasa_politica_monetaria_router = APIRouter()

@tasa_politica_monetaria_router.get("/")
async def get_tasa_politica_monetaria(client: HttpxClientDep, cache_store: CacheDep):
    tasa_value = await cache_store.get_from_cache("tasa-politica-monetaria")
    if tasa_value is not None:
        return {"tasa_politica_monetaria": tasa_value}

    tasa_value = await get_tasa_politica_monetaria_service(client)
    await cache_store.add_to_cache("tasa-politica-monetaria", tasa_value, ttl=86400)
    return {"tasa_politica_monetaria": tasa_value}
