import httpx
from bs4 import BeautifulSoup

from app.threading import run_in_thread
from app.utils import extract_price, extract_text, get_page_html


def _parse_iccv_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("section", attrs={"aria-label": "ICCV actual"})
    if section is None:
        return {"variacion_anual": None, "variacion_mensual": None, "indice_general": None}

    articles = section.find_all("article")
    result: dict[str, dict | None] = {
        "variacion_anual": None,
        "variacion_mensual": None,
        "indice_general": None,
    }

    for article in articles:
        heading = extract_text(article.find("h2"))
        price_div = article.find("div", class_="text-brand") or article.find("div", class_="font-bold")
        unit = extract_text(article.find("p", class_="text-gray-500"))

        price = extract_price(extract_text(price_div)) if price_div else None

        entry = {"valor": price, "detalle": unit}

        if "anual" in heading.lower():
            result["variacion_anual"] = entry
        elif "mensual" in heading.lower():
            result["variacion_mensual"] = entry
        elif "índice" in heading.lower() or "indice" in heading.lower():
            result["indice_general"] = entry

    return result


async def get_iccv_service(client: httpx.AsyncClient) -> dict:
    html = await get_page_html("indice-costo-construccion-vivienda", client)
    return await run_in_thread(_parse_iccv_html, html)
