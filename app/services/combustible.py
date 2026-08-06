import httpx

from app.utils import extract_price, get_metric_cards, get_page_html, get_row_header


async def get_combustible_service(client: httpx.AsyncClient) -> dict:
    """The combustible page lists one card per fuel in its "precios" row,
    each with a price and the unit it applies to ("/litro").
    """
    html = await get_page_html("combustible", client)
    header = await get_row_header(html)
    cards = await get_metric_cards(html, "precios")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "precios": [
            {
                "combustible": card["nombre"],
                "precio": extract_price(card["valor"]),
                "unidad": card["detalle"],
            }
            for card in cards
        ],
    }
