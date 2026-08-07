from app.utils import get_page_html, get_span_element
import httpx

# The euro page shows its value in the same green span as /dolar.
async def get_euro_service(client: httpx.AsyncClient):
    html = await get_page_html("euro", client)
    euro_value = await get_span_element(html, "font-semibold text-green-600")
    return euro_value
