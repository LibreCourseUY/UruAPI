from fastapi import APIRouter, Depends
import httpx

from app.services.iccv import get_iccv_service
from app.routers import get_client

router = APIRouter(
    tags=["iccv"],
)


@router.get("/indice-costo-construccion-vivienda/")
async def indice_costo_construccion_vivienda(client: httpx.AsyncClient = Depends(get_client)) -> dict:
    """Devuelve el Índice de Costo de la Construcción de Vivienda (ICCV) de Uruguay."""
    return await get_iccv_service(client)
