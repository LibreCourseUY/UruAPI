import httpx
from bs4 import BeautifulSoup

from app.threading import run_in_thread
from app.utils import extract_price, extract_text, get_page_html


def _parse_inflacion_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find("header", class_="text-center")
    if header is None:
        return {"total_pais": None, "montevideo": None, "interior": None}

    divs = header.find_all("div", class_="text-center")
    result: dict[str, float | None] = {
        "total_pais": None,
        "montevideo": None,
        "interior": None,
    }

    for div in divs:
        label = extract_text(div.find("p", class_="font-medium") or div.find("p", class_="text-sm"))
        price = extract_price(extract_text(div.find("p", class_="font-bold") or div.find("p", class_="font-semibold")))

        if "Total" in label:
            result["total_pais"] = price
        elif "Montevideo" in label:
            result["montevideo"] = price
        elif "Interior" in label:
            result["interior"] = price

    return result


async def get_inflacion_service(client: httpx.AsyncClient) -> dict:
    html = await get_page_html("inflacion", client)
    return await run_in_thread(_parse_inflacion_html, html)
