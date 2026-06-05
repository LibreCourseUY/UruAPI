from fastapi import APIRouter

from app.services.supergas import get_supergas_service
from app.utils import HttpxClientDep

supergas_router = APIRouter()


@supergas_router.get("/")
async def get_supergas(client: HttpxClientDep):
    supergas_value = await get_supergas_service(client)
    return {"supergas": supergas_value}
