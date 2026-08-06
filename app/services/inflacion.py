import httpx

from app.utils import get_metric_cards, get_page_html, get_row_header


async def get_inflacion_service(client: httpx.AsyncClient) -> dict:
    """Unlike the other indicator pages, /inflacion puts its figures inside the
    header row instead of a "kpis" row. The national figure is rendered bold and
    the two regional ones semibold, so each weight is collected separately.
    """
    html = await get_page_html("inflacion", client)
    header = await get_row_header(html)
    total_pais = await get_metric_cards(html, "header")
    regiones = await get_metric_cards(html, "header", value_class="font-semibold")

    return {
        "titulo": header["titulo"],
        "fuente": header["detalle"],
        "total_pais": total_pais[0]["valor"] if total_pais else None,
        "regiones": [
            {"nombre": region["nombre"], "valor": region["valor"]}
            for region in regiones
        ],
    }
