import httpx
from bs4 import BeautifulSoup

from app.threading import run_in_thread
from app.utils import extract_price, extract_text, get_page_html


def _parse_peajes_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("section", attrs={"aria-label": "Tarifas actuales de peajes"})
    if section is None:
        return {"telepeaje": None, "sucive": None}

    articles = section.find_all("article")
    result: dict[str, dict | None] = {"telepeaje": None, "sucive": None}

    for article in articles:
        heading = extract_text(article.find("h2"))
        price_div = article.find("div", class_="text-brand")
        unit = extract_text(article.find("p", class_="text-gray-500")).lstrip("/")

        price = extract_price(extract_text(price_div)) if price_div else None

        entry = {"precio": price, "unidad": unit if unit else "sentido"}

        if "Telepeaje" in heading:
            result["telepeaje"] = entry
        elif "SUCIVE" in heading:
            result["sucive"] = entry

    return result


async def get_peajes_service(client: httpx.AsyncClient) -> dict:
    html = await get_page_html("peajes", client)
    return await run_in_thread(_parse_peajes_html, html)
