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


# Prices render in the Uruguayan format: "." groups thousands, "," is the
# decimal separator ("$1.216,28"). The thousands group is matched greedily so
# the number is not truncated at the first ".".
GROUPED_AMOUNT = r"\d{1,3}(?:\.\d{3})+(?:,\d+)?"
PRICE_PATTERN = rf"\$\s*({GROUPED_AMOUNT}|\d+(?:[.,]\d+)?)"


def parse_amount(amount: str) -> float:
    """Turn a Uruguayan-formatted amount ("1.216,28") into a float."""
    if re.fullmatch(GROUPED_AMOUNT, amount):
        return float(amount.replace(".", "").replace(",", "."))

    return float(amount.replace(",", "."))


def extract_price(text: str) -> float | None:
    price_match = re.search(PRICE_PATTERN, text)
    if price_match is None:
        return None

    return parse_amount(price_match.group(1))


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


def _normalize_whitespace(element: Tag | None) -> str:
    """Source markup wraps sentences across lines, so collapse the runs."""
    if element is None:
        return ""

    return " ".join(element.get_text(" ", strip=True).split())


HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


def _has_class(element: Tag, class_token: str) -> bool:
    return class_token in (element.get("class") or [])


def _get_row_section(soup: BeautifulSoup, row: str) -> Tag | None:
    """Pages on datosuruguay.com wrap each block in <section data-duy-row="...">."""
    return soup.find("section", attrs={"data-duy-row": row})


def _parse_metric_cards(html: str, row: str, value_class: str) -> list[dict]:
    """Extract the label/value cards of a row section.

    Every card renders the same way: a label node (an <h2> or a small <p>)
    followed by a sibling holding the number, tagged with `value_class`
    (`font-bold` on most pages). Heading tags are never treated as values so
    the section title is not mistaken for a metric.
    """
    soup = BeautifulSoup(html, "html.parser")
    section = _get_row_section(soup, row)
    if section is None:
        return []

    cards: list[dict] = []
    for value_element in section.find_all(lambda tag: _has_class(tag, value_class)):
        if value_element.name in HEADING_TAGS:
            continue

        details = [extract_text(sibling) for sibling in value_element.find_next_siblings()]

        cards.append(
            {
                "nombre": extract_text(value_element.find_previous_sibling()),
                "valor": extract_text(value_element),
                "detalle": " ".join(detail for detail in details if detail),
            }
        )

    return cards


async def get_metric_cards(html: str, row: str, value_class: str = "font-bold") -> list[dict]:
    return await run_in_thread(_parse_metric_cards, html, row, value_class)


def _get_row_text(html: str, row: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return _normalize_whitespace(_get_row_section(soup, row))


async def get_row_text(html: str, row: str) -> str:
    """Return the whole row section as flat text, for notes that sit outside the cards."""
    return await run_in_thread(_get_row_text, html, row)


def _parse_row_header(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    section = _get_row_section(soup, "header")
    if section is None:
        return {"titulo": "", "detalle": ""}

    paragraphs = section.find_all("p")

    return {
        "titulo": _normalize_whitespace(section.find("h1")),
        "detalle": _normalize_whitespace(paragraphs[-1] if paragraphs else None),
    }


async def get_row_header(html: str) -> dict:
    """Return the <h1> title and trailing source line of the header row."""
    return await run_in_thread(_parse_row_header, html)
