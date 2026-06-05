from fastapi import APIRouter

from app.services.doble_horario import get_doble_horario_service
from app.utils import HttpxClientDep

doble_horario_router = APIRouter()


@doble_horario_router.get("/")
async def get_doble_horario(client: HttpxClientDep):
    tarifas = await get_doble_horario_service(client)
    return {"tarifa_doble_horario": tarifas}
