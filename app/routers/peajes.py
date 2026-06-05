from fastapi import APIRouter, Depends
import httpx

from app.services.peajes import get_peajes_service
from app.routers import get_client

router = APIRouter(
    tags=["peajes"],
)


@router.get("/peajes/")
async def peajes(client: httpx.AsyncClient = Depends(get_client)) -> dict:
    """Devuelve las tarifas de peajes (Telepeaje y SUCIVE) en Uruguay."""
    return await get_peajes_service(client)
