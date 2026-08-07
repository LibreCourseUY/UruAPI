from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import (
    boleto_router,
    combustible_router,
    dolar_router,
    euro_router,
    indice_costo_construccion_vivienda_router,
    inflacion_router,
    ipc_router,
    pbi_router,
    peajes_router,
    real_router,
    supergas_router,
    tarifa_electrica_router,
    tasa_politica_monetaria_router,
    ui_router,
    ur_router,
    utils_router,
)

app = FastAPI()

app.include_router(router=utils_router, prefix="/utils")
app.include_router(router=dolar_router, prefix="/dolar")
app.include_router(router=boleto_router, prefix="/boleto")
app.include_router(router=supergas_router, prefix="/supergas")
app.include_router(router=real_router, prefix="/real")
app.include_router(router=ur_router, prefix="/ur")
app.include_router(router=euro_router, prefix="/euro")
app.include_router(router=ui_router, prefix="/ui")
app.include_router(router=tasa_politica_monetaria_router, prefix="/tasa-politica-monetaria")
app.include_router(router=tarifa_electrica_router, prefix="/tarifa-electrica")
app.include_router(router=ipc_router, prefix="/ipc")
app.include_router(router=pbi_router, prefix="/pbi")
app.include_router(router=peajes_router, prefix="/peajes")
app.include_router(router=combustible_router, prefix="/combustible")
app.include_router(
    router=indice_costo_construccion_vivienda_router,
    prefix="/indice-costo-construccion-vivienda",
)
app.include_router(router=inflacion_router, prefix="/inflacion")

@app.get("/")
def root():
    return RedirectResponse("/docs")
