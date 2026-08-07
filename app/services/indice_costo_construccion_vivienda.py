import httpx

from app.utils import get_metric_cards, get_page_html, get_row_header

# The ICCV cards render a bare dash when the INE has not published the figure yet.
PLACEHOLDER_VALUES = {"-", "--", "s/d"}


def _clean_value(valor: str) -> str | None:
    return None if valor in PLACEHOLDER_VALUES else valor


async def get_indice_costo_construccion_vivienda_service(client: httpx.AsyncClient) -> dict:
    """The ICCV page shows three cards in its "kpis" row: yearly variation,
    monthly variation and the general index.
    """
    html = await get_page_html("indice-costo-construccion-vivienda", client)
    header = await get_row_header(html)
    cards = await get_metric_cards(html, "kpis")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "indicadores": [
            {
                "nombre": card["nombre"],
                "valor": _clean_value(card["valor"]),
                "detalle": card["detalle"],
            }
            for card in cards
        ],
    }
