from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, Request


def build_httpx_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        headers={"User-Agent": "Mozilla/5.0 ..."},
        timeout=httpx.Timeout(10.0, connect=5.0),
        follow_redirects=True,
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5))


@asynccontextmanager
async def httpx_client_lifespan(app: FastAPI):
    """Build the client once for the whole app.

    Constructing an AsyncClient loads the CA bundle and builds an SSL context,
    which costs hundreds of milliseconds. Doing that per request made every
    cache hit pay the price of a network call it never made, and threw away
    connection pooling between requests.
    """
    async with build_httpx_client() as client:
        app.state.httpx_client = client
        yield


async def get_httpx_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.httpx_client


HttpxClientDep = Annotated[httpx.AsyncClient, Depends(get_httpx_client)]
