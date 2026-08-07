import re

import httpx
from bs4 import BeautifulSoup, Tag

from app.threading import run_in_thread
from app.utils import extract_price, extract_text, get_page_html


def _get_ticket_type(item: Tag) -> str:
    return extract_text(item.find("span", class_="font-medium"), "Unknown")


def _extract_efectivo_price(item: Tag) -> float | None:
    efectivo_match = re.search(r"Efectivo:\s*\$(\d+(?:[.,]\d+)?)", extract_text(item))
    if efectivo_match is None:
        return None

    return float(efectivo_match.group(1).replace(",", "."))


def _extract_tarjeta_price(item: Tag) -> float | None:
    price_container = item.find("div", class_="text-right")
    if price_container is None:
        return None

    for candidate in price_container.find_all("div"):
        price = extract_price(extract_text(candidate))
        if price is not None:
            return price

    return None


def _extract_ticket(item: Tag) -> dict:
    ticket_text = extract_text(item)

    return {
        "ticket_type": _get_ticket_type(item),
        "tarjeta": _extract_tarjeta_price(item),
        "efectivo": _extract_efectivo_price(item),
        "gratis": "Gratis" in ticket_text,
    }


def _extract_section_tickets(soup: BeautifulSoup, row: str) -> list[dict]:
    section = soup.find("section", attrs={"data-duy-row": row})
    if section is None:
        return []

    items_container = section.find("div", class_="divide-y divide-gray-200")
    if items_container is None:
        return []

    tickets: list[dict] = []
    for item in items_container.find_all("div", recursive=False):
        ticket = _extract_ticket(item)
        if ticket["ticket_type"] != "Unknown":
            tickets.append(ticket)

    return tickets


def _parse_boleto_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    fecha_select = soup.find("select", id="fecha-select")
    selected_option = fecha_select.find("option", selected=True) if fecha_select else None
    if selected_option is None and fecha_select is not None:
        selected_option = fecha_select.find("option")

    vigencia_section = soup.find("section", attrs={"data-duy-row": "tarifas"})
    vigencia_title = extract_text(
        vigencia_section.find("h2", class_="text-lg md:text-xl font-semibold text-gray-900") if vigencia_section else None
    )

    return {
        "vigencia": {
            "fecha": selected_option.get("value", "") if selected_option else "",
            "detalle": vigencia_title,
        },
        "tarifas": {
            "generales": _extract_section_tickets(soup, "tarifas"),
            "especiales": _extract_section_tickets(soup, "tarifas_especiales"),
        },
    }


async def get_boleto_service(client: httpx.AsyncClient) -> dict:
    html = await get_page_html("boleto", client)
    return await run_in_thread(_parse_boleto_html, html)
