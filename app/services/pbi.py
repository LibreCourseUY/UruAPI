import httpx

from app.utils import get_metric_cards, get_page_html, get_row_header


async def get_pbi_service(client: httpx.AsyncClient) -> dict:
    """The PBI page shows the latest quarter in its "kpis" row: the real
    year-on-year variation and the PIB at current prices.
    """
    html = await get_page_html("pbi", client)
    header = await get_row_header(html)
    indicadores = await get_metric_cards(html, "kpis")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "indicadores": indicadores,
    }
