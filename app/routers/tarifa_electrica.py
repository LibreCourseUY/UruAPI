from fastapi import APIRouter

from app.services.tarifa_electrica import (
    get_doble_horario_service,
    get_residencial_simple_service,
    get_triple_horario_service,
)
from app.utils import HttpxClientDep
from app.cache import CacheDep

tarifa_electrica_router = APIRouter()

@tarifa_electrica_router.get("/residencial-simple/")
async def get_residencial_simple(client: HttpxClientDep, cache_store: CacheDep):
    tarifa = await cache_store.get_from_cache("tarifa-electrica:residencial-simple")
    if tarifa is not None:
        return tarifa

    tarifa = await get_residencial_simple_service(client)
    await cache_store.add_to_cache("tarifa-electrica:residencial-simple", tarifa, ttl=86400)
    return tarifa


@tarifa_electrica_router.get("/doble-horario/")
async def get_doble_horario(client: HttpxClientDep, cache_store: CacheDep):
    tarifa = await cache_store.get_from_cache("tarifa-electrica:doble-horario")
    if tarifa is not None:
        return tarifa

    tarifa = await get_doble_horario_service(client)
    await cache_store.add_to_cache("tarifa-electrica:doble-horario", tarifa, ttl=86400)
    return tarifa


@tarifa_electrica_router.get("/triple-horario/")
async def get_triple_horario(client: HttpxClientDep, cache_store: CacheDep):
    tarifa = await cache_store.get_from_cache("tarifa-electrica:triple-horario")
    if tarifa is not None:
        return tarifa

    tarifa = await get_triple_horario_service(client)
    await cache_store.add_to_cache("tarifa-electrica:triple-horario", tarifa, ttl=86400)
    return tarifa
