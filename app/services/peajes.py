import httpx

from app.utils import extract_price, get_metric_cards, get_page_html, get_row_header


async def get_peajes_service(client: httpx.AsyncClient) -> dict:
    """The peajes page lists one card per payment method in its "kpis" row,
    each with a price and the unit it applies to ("/sentido").
    """
    html = await get_page_html("peajes", client)
    header = await get_row_header(html)
    cards = await get_metric_cards(html, "kpis")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "tarifas": [
            {
                "modalidad": card["nombre"],
                "precio": extract_price(card["valor"]),
                "unidad": card["detalle"],
            }
            for card in cards
        ],
    }
