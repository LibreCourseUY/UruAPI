from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import boleto_router, dolar_router, supergas_router, utils_router

app = FastAPI()

app.include_router(router=utils_router, prefix="/utils")
app.include_router(router=dolar_router, prefix="/dolar")
app.include_router(router=boleto_router, prefix="/boleto")
app.include_router(router=supergas_router, prefix="/supergas")


@app.get("/")
def root():
    return RedirectResponse("/docs")
