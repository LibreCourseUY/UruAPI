import re

import httpx

from app.utils import extract_price, get_metric_cards, get_page_html, get_row_header, get_row_text

# The footer under the price cards reads:
# "Cargo fijo $488,00/mes · Cargo de potencia $83,20/kW · Precios sin IVA (...)"
CARGO_FIJO_PATTERN = r"Cargo fijo\s*\$(\d+(?:[.,]\d+)?)"
CARGO_POTENCIA_PATTERN = r"Cargo de potencia\s*\$(\d+(?:[.,]\d+)?)"


def _extract_cargo(text: str, pattern: str) -> float | None:
    cargo_match = re.search(pattern, text)
    if cargo_match is None:
        return None

    return float(cargo_match.group(1).replace(".", "").replace(",", "."))


async def _get_tarifa_electrica_service(modalidad: str, client: httpx.AsyncClient) -> dict:
    """Every /tarifa-electrica page shares one layout: a header row with the
    modality name and validity date, and a "current_prices" row holding one
    card per price tier plus a footer line with the fixed and power charges.
    """
    html = await get_page_html(f"tarifa-electrica/{modalidad}", client)
    header = await get_row_header(html)
    cards = await get_metric_cards(html, "current_prices")
    # The charges live in a footer paragraph next to the card grid, not in a card.
    cargos_text = await get_row_text(html, "current_prices")

    return {
        "modalidad": header["titulo"],
        "vigencia": header["detalle"],
        "tramos": [
            {"concepto": card["nombre"], "precio": extract_price(card["valor"])}
            for card in cards
        ],
        "cargo_fijo": _extract_cargo(cargos_text, CARGO_FIJO_PATTERN),
        "cargo_potencia": _extract_cargo(cargos_text, CARGO_POTENCIA_PATTERN),
    }


async def get_residencial_simple_service(client: httpx.AsyncClient) -> dict:
    return await _get_tarifa_electrica_service("residencial-simple", client)


async def get_doble_horario_service(client: httpx.AsyncClient) -> dict:
    return await _get_tarifa_electrica_service("doble-horario", client)


async def get_triple_horario_service(client: httpx.AsyncClient) -> dict:
    return await _get_tarifa_electrica_service("triple-horario", client)
