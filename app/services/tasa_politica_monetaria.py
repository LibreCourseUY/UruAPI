from app.utils import get_div_element, get_page_html
import httpx

# The TPM page has no green value span like /dolar. The current rate is the big
# number in the "TPM vigente" card of the kpis row.
async def get_tasa_politica_monetaria_service(client: httpx.AsyncClient):
    html = await get_page_html("tasa-politica-monetaria", client)
    tasa_value = await get_div_element(html, "text-4xl md:text-6xl font-bold text-brand")
    return tasa_value
