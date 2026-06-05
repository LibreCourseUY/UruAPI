import httpx

from app.utils import get_page_html, get_all_p_elements


async def get_triple_horario_service(client: httpx.AsyncClient):
    html = await get_page_html("tarifa-electrica/triple-horario", client)
    labels = await get_all_p_elements(html, "text-xs text-gray-500 mb-1")
    prices = await get_all_p_elements(html, "font-bold text-brand")
    return dict(zip(labels, prices))
