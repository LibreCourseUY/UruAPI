# Contributing to UruAPI

Thanks for contributing.

This project is still small, so the easiest way to add a new endpoint is to follow the same pattern used by the existing `/dolar` route.

This guide is specific to `UruAPI`, but it should be read together with the general [LibreCourseUY contribution guide](https://github.com/LibreCourseUY/.github/blob/master/CONTRIBUTING.md).

## Before You Start

Before contributing, make sure your change also follows the broader LibreCourseUY expectations:

- keep changes small, focused, and easy to review
- check whether an issue already exists before starting large work
- update documentation when behavior changes
- avoid mixing unrelated refactors into a small feature or fix
- explain clearly what changed and why

If you are new, start with one small endpoint or one small documentation improvement.

It is strongly recommended to check the repository's [good first issue](https://github.com/LibreCourseUY/UruAPI/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22) list before starting work.

Those issues are usually the best entry point for new contributors because they are already scoped and documented.

## Commit Message Pattern

This repository uses Conventional Commits.

Pattern:

```text
type(scope): short description
```

Common examples:

```text
feat(routes): add /euro endpoint
fix(dolar): await scraper helpers in service
docs(readme): update docker instructions
refactor(utils): simplify HTML parsing helpers
```

Common commit types:

- `feat`: new functionality
- `fix`: bug fix
- `docs`: documentation-only change
- `refactor`: internal code change without changing behavior
- `test`: tests added or updated
- `chore`: maintenance work

Rules:

- keep the subject short and clear
- use lowercase commit types
- describe what changed, not what you were trying to do
- prefer one focused commit per logical change when possible

## Creating A New Indicator Route

The current pattern is split into 3 layers:

1. Router layer
2. Service layer
3. Shared scraping helpers

### 1. Router Layer

The router is responsible for:

- defining the URL
- receiving FastAPI dependencies
- calling the service
- returning a JSON-friendly response

Example from `app/routers/dolar.py`:

```python
from fastapi import APIRouter

from app.services.dolar import get_dolar_service
from app.utils import HttpxClientDep

dolar_router = APIRouter()


@dolar_router.get("/")
async def get_dolar(client: HttpxClientDep):
    dolar_value = await get_dolar_service(client)
    return {"dolar": dolar_value}
```

Important rules:

- The route function should usually be `async def`.
- If the service is async, always use `await`.
- `HttpxClientDep` must be in the function signature, not passed manually.
- Returning a Python `dict` is correct in FastAPI. FastAPI converts it to JSON automatically.

### 2. Service Layer

The service is responsible for the scraping logic for one endpoint.

Example from `app/services/dolar.py`:

```python
import httpx

from app.utils import get_page_html, get_span_element


async def get_dolar_service(client: httpx.AsyncClient):
    html = await get_page_html("dolar", client)
    dolar_value = await get_span_element(html, "font-semibold text-green-600")
    return dolar_value
```

Important rules:

- The service should receive a real `httpx.AsyncClient`.
- Do not pass `HttpxClientDep` into the service.
- Always `await` async helper calls.
- Keep the service focused on one indicator.

### 3. Shared Scraping Helpers

Helpers live in `app/utils/scrapper.py`.

Current helpers:

- `get_page_html()` fetches the page HTML
- `get_element_text()` extracts text from a given HTML tag and class
- `get_span_element()` is a convenience wrapper for `<span>` elements
- `get_div_element()` is a convenience wrapper for `<div>` elements
- `extract_price()` parses price strings like `$52,00` into floats

These helpers already use `run_in_thread()` for BeautifulSoup parsing.

## Simple Vs Complex Routes

There are currently two route families in this project:

1. simple `/dolar`-style routes
2. more complex `/boleto`-style routes

If you are new, start with a simple route first.

Examples of simple routes:

- `/dolar`
- `/supergas`
- `/tarifa-electrica/residencial-simple`
- `/tarifa-electrica/doble-horario`
- `/tarifa-electrica/triple-horario`

Examples of more complex routes:

- `/boleto`
- `/ipc`
- `/indice-costo-construccion-vivienda`
- `/inflacion`
- `/pbi`
- `/combustible`
- `/peajes`

### Simple `/dolar`-Style Routes

Use this pattern when:

- the page only needs one main value
- the value can be extracted with one simple selector
- the response is a small dict like `{"dolar": "40.25"}`

These routes usually need:

1. one router
2. one service
3. one or two generic scraper helpers

### Complex `/boleto`-Style Routes

Use this pattern when:

- the page contains repeated blocks
- the response needs multiple grouped values
- there are optional prices or special cases like `Gratis`
- you need to parse sections, cards, or lists instead of one value

For these routes, do not try to solve everything with repeated calls to `get_span_element()`.

Instead:

1. fetch the page once with `get_page_html()`
2. parse the full HTML in the service layer
3. group the data into a clean JSON structure
4. keep generic helpers in `app/utils/scrapper.py`
5. keep page-specific parsing logic in the service file

The current reference implementation for this style is `/boleto`.

### Complex Route Checklist

For a boleto-style route, the service should usually:

1. fetch the HTML once
2. parse the document once
3. identify the major sections
4. extract repeated items into a list of dicts
5. normalize prices and missing values
6. return a structure that is easy for API consumers to use

Recommended approach:

- generic parsing helpers in `app/utils/scrapper.py`
- route-specific extraction logic in `app/services/<route>.py`
- minimal HTTP logic in `app/routers/<route>.py`

### Example Complex Response Shape

```json
{
  "vigencia": {
    "fecha": "2026-01-05",
    "detalle": "Tarifas vigentes desde January 05, 2026"
  },
  "tarifas": {
    "generales": [
      {
        "ticket_type": "Común 1 hora",
        "tarjeta": 52.0,
        "efectivo": 64.0,
        "gratis": false
      }
    ],
    "especiales": [
      {
        "ticket_type": "Escolar",
        "tarjeta": null,
        "efectivo": null,
        "gratis": true
      }
    ]
  }
}
```

This grouped-by-ticket-type style is preferred for more complex tariff endpoints.

## File Changes Needed For A New Route

When adding a new indicator endpoint, you will usually touch these files:

1. Create a new service file in `app/services/`
2. Create a new router file in `app/routers/`
3. Export the router from `app/routers/__init__.py`
4. Register the router in `app/main.py`

### Example Checklist

If you want to add `/euro`, the work usually looks like this:

1. Create `app/services/euro.py`
2. Create `app/routers/euro.py`
3. Add `from .euro import euro_router` to `app/routers/__init__.py`
4. Add `app.include_router(router=euro_router, prefix="/euro")` to `app/main.py`
5. Reuse the same helper pattern as `/dolar`

## Starter Template

### Service template

```python
import httpx

from app.utils import get_page_html, get_span_element


async def get_example_service(client: httpx.AsyncClient):
    html = await get_page_html("example-endpoint", client)
    value = await get_span_element(html, "your-css-class")
    return value
```

### Router template

```python
from fastapi import APIRouter

from app.services.example import get_example_service
from app.utils import HttpxClientDep

example_router = APIRouter()


@example_router.get("/")
async def get_example(client: HttpxClientDep):
    value = await get_example_service(client)
    return {"example": value}
```

## How To Pick The Right Scraper Helper

Use the browser devtools on `datosuruguay.com` and inspect the element you want.

If the value is inside:

- a `<span>`, use `get_span_element()`
- a `<div>`, use `get_div_element()`

If you need a different tag but still only want a single value, use `get_element_text()`.

If neither works, add a new helper only if needed.

## Common Mistakes

### Mistake: Returning a coroutine

Wrong:

```python
value = get_example_service(client)
return {"value": value}
```

Correct:

```python
value = await get_example_service(client)
return {"value": value}
```

### Mistake: Passing `HttpxClientDep` manually

Wrong:

```python
value = await get_example_service(HttpxClientDep)
```

Correct:

```python
async def get_example(client: HttpxClientDep):
    value = await get_example_service(client)
```

### Mistake: Mixing routing and scraping logic

Keep this split:

- router: HTTP concerns
- service: indicator-specific scraping logic
- utils: shared helpers

## Running The App

### Local

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8083
```

### Docker

```bash
docker compose up --build
```

## Quick Review Checklist

Before opening a PR, check:

1. The new router is imported in `app/routers/__init__.py`
2. The new router is registered in `app/main.py`
3. Async calls are awaited
4. The route returns a `dict`
5. The endpoint appears in `http://localhost:8083/docs`
