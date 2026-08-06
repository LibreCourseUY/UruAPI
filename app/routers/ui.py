from fastapi import APIRouter

from app.services.ui import get_ui_service
from app.utils import HttpxClientDep
from app.cache import CacheDep

ui_router = APIRouter()

@ui_router.get("/")
async def get_ui(client: HttpxClientDep, cache_store: CacheDep):
    ui_value = await cache_store.get_from_cache("ui")
    if ui_value is not None:
        return {"ui": ui_value}

    ui_value = await get_ui_service(client)
    await cache_store.add_to_cache("ui", ui_value, ttl=86400)
    return {"ui": ui_value}
