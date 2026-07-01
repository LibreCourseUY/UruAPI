from app.utils import get_page_html, get_span_element
import httpx

async def get_real_service(client : httpx.AsyncClient):
    html = await get_page_html("real", client)
    real_value = await get_span_element(html, "font-semibold text-green-600")
    return real_value
