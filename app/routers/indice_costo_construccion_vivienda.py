from fastapi import APIRouter

from app.services.indice_costo_construccion_vivienda import (
    get_indice_costo_construccion_vivienda_service,
)
from app.utils import HttpxClientDep
from app.cache import CacheDep

indice_costo_construccion_vivienda_router = APIRouter()

@indice_costo_construccion_vivienda_router.get("/")
async def get_indice_costo_construccion_vivienda(client: HttpxClientDep, cache_store: CacheDep):
    iccv_data = await cache_store.get_from_cache("indice-costo-construccion-vivienda")
    if iccv_data is not None:
        return iccv_data

    iccv_data = await get_indice_costo_construccion_vivienda_service(client)
    await cache_store.add_to_cache("indice-costo-construccion-vivienda", iccv_data, ttl=86400)
    return iccv_data
