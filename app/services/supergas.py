from app.utils import get_page_html, get_span_element
import httpx

async def get_supergas_service(client : httpx.AsyncClient):
    html = await get_page_html("supergas", client)
    supergas_value = await get_span_element(html, "font-semibold text-brand")
    return supergas_value
