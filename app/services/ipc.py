import httpx

from app.utils import get_metric_cards, get_page_html, get_row_header


async def get_ipc_service(client: httpx.AsyncClient) -> dict:
    """The IPC page exposes three cards in its "kpis" row: monthly variation,
    year-on-year variation and the accumulated inflation for the year.
    Values are kept as the source renders them ("+0,0657%") so consumers can
    decide how to parse a percentage.
    """
    html = await get_page_html("ipc", client)
    header = await get_row_header(html)
    indicadores = await get_metric_cards(html, "kpis")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "indicadores": indicadores,
    }
