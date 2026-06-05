from fastapi import APIRouter

from app.services.residencial_simple import get_residencial_simple_service
from app.utils import HttpxClientDep

residencial_simple_router = APIRouter()


@residencial_simple_router.get("/")
async def get_residencial_simple(client: HttpxClientDep):
    tarifas = await get_residencial_simple_service(client)
    return {"tarifa_residencial_simple": tarifas}
