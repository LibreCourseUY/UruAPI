from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import (
    boleto_router,
    doble_horario_router,
    dolar_router,
    residencial_simple_router,
    supergas_router,
    triple_horario_router,
    utils_router,
)

app = FastAPI()

app.include_router(router=utils_router, prefix="/utils")
app.include_router(router=dolar_router, prefix="/dolar")
app.include_router(router=boleto_router, prefix="/boleto")
app.include_router(router=supergas_router, prefix="/supergas")
app.include_router(router=residencial_simple_router, prefix="/tarifa-electrica/residencial-simple")
app.include_router(router=triple_horario_router, prefix="/tarifa-electrica/triple-horario")
app.include_router(router=doble_horario_router, prefix="/tarifa-electrica/doble-horario")


@app.get("/")
def root():
    return RedirectResponse("/docs")
