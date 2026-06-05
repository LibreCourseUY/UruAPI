from fastapi import APIRouter, Depends
import httpx

from app.services.inflacion import get_inflacion_service
from app.routers import get_client

router = APIRouter(
    tags=["inflacion"],
)


@router.get("/inflacion/")
async def inflacion(client: httpx.AsyncClient = Depends(get_client)) -> dict:
    """Devuelve la inflación actual de Uruguay (Total País, Montevideo, Interior)."""
    return await get_inflacion_service(client)
