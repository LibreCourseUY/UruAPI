from fastapi import APIRouter

from app.services.triple_horario import get_triple_horario_service
from app.utils import HttpxClientDep

triple_horario_router = APIRouter()


@triple_horario_router.get("/")
async def get_triple_horario(client: HttpxClientDep):
    tarifas = await get_triple_horario_service(client)
    return {"tarifa_triple_horario": tarifas}
