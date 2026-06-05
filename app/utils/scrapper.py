import re

import httpx
from bs4 import BeautifulSoup, Tag

from app.threading import run_in_thread

async def get_page_html(endpoint :  str, client : httpx.AsyncClient):
    page = await client.get(url=f"https://datosuruguay.com/{endpoint}")
    html = page.text
    return html


def extract_text(element: Tag | None, default: str = "") -> str:
    if element is None:
        return default

    return element.get_text(strip=True)


def extract_price(text: str) -> float | None:
    price_match = re.search(r"\$(\d+(?:[.,]\d+)?)", text)
    if price_match is None:
        return None

    return float(price_match.group(1).replace(",", "."))


def _get_element_text(html: str, tag: str, element_class: str, default: str = "") -> str:
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find(tag, class_=element_class)
    return extract_text(element, default)


async def get_element_text(html: str, tag: str, element_class: str, default: str = "") -> str:
    return await run_in_thread(_get_element_text, html, tag, element_class, default)


async def get_span_element(html: str, element_class: str, default: str = "") -> str:
    return await get_element_text(html, "span", element_class, default)


async def get_div_element(html: str, element_class: str, default: str = "") -> str:
    return await get_element_text(html, "div", element_class, default)


def _get_all_elements_text(html: str, tag: str, element_class: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all(tag, class_=element_class)
    return [extract_text(el) for el in elements]


async def get_all_span_elements(html: str, element_class: str) -> list[str]:
    return await run_in_thread(_get_all_elements_text, html, "span", element_class)


async def get_all_p_elements(html: str, element_class: str) -> list[str]:
    return await run_in_thread(_get_all_elements_text, html, "p", element_class)
