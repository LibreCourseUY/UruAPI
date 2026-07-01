from fastapi import APIRouter

from app.services.real import get_real_service
from app.utils import HttpxClientDep

real_router = APIRouter()

@real_router.get("/")
async def get_real(client :  HttpxClientDep):
    real_value = await get_real_service(client)
    return {"real" : real_value}
