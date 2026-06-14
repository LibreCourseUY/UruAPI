# UruAPI

> **⚠️ Important**
>
> LibreCourseUY is an open source, independent and community-driven software project. The tools, features and resources available on this platform including "UruAPI" were created and maintained by members, contributors and collaborators of LibreCourseUY.
>
> The "UruAPI" tool is not affiliated with, associated with, sponsored by, endorsed by, authorized by, or supported by datosuruguay.com or any institution or organization, including but not limited to the Central Bank of Uruguay (BCU), the National Statistics Institute (INE) and the Social Security Bank (BPS).
>
> Any reference to names, acronyms, trademarks, sources or institutions is used solely for descriptive and informational purposes, and does not imply any institutional relationship, approval or official status.
>
> The software and associated content are provided "AS IS", without warranties of any kind. The data may contain errors, delays or inaccuracies; it must not be used as an official source. Use of this project is at your own risk.
>
> By continuing, you acknowledge and accept these terms, and that any interpretation of officiality is incorrect.

Welcome to UruAPI! An API that wraps [datosuruguay.com](https://datosuruguay.com/), giving programmatic access to Uruguay's daily economic indicators.

## What is this project?

UruAPI is a wrapper around [datosuruguay.com](https://datosuruguay.com/) and exposes Uruguay's daily-updated economic indicators in a clean, JSON-friendly format.

All data originates from official sources_ the Central Bank of Uruguay (BCU), the National Statistics Institute (INE), and the Social Security Bank (BPS). See the full list in the datosuruguay.com [methodology](https://datosuruguay.com/metodologia).

### Data available

- **Exchange rates**: USD, EUR, BRL, ARS
- **Price indices**: Inflation (IPC) and Unidad Indexada (UI)
- **Fuel & transport**: ANCAP fuel, Montevideo transit (STM), tolls
- **Social security**: BPS indices, pensions, family allowances

### Tech Stack

- **Language**: Python 3.11 or higher
- **Framework**: FastAPI
- **Dependency Management**: uv

## How to Install and Run

### Prerequisites

- Python 3.11 or higher: [Link](https://www.python.org/downloads/)
- uv: [Link](https://docs.astral.sh/uv/getting-started/installation/)

### Local Development Setup

1. Enter the project folder:
   ```bash
   cd UruAPI
   ```

2. Install dependencies with uv:
   ```bash
   uv sync
   ```

3. Run the development server:
   ```bash
   uv run uvicorn app.main:app --reload --port 8083
   ```

### Interactive API docs

Once the server is running, you can view the automatic documentation at:

- Swagger UI: `http://localhost:8083/docs`

### With Docker

1. Build and start the container:
   ```bash
   docker compose up --build
   ```

2. Stop the container:
   ```bash
   docker compose down
   ```

The API will be available at `http://localhost:8083`.

## Project Structure

```
UruAPI/
├── app/                     # Main application package
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings (cache backend, Redis URL, ...)
│   ├── threading.py         # Async helpers for thread offloading
│   ├── cache/               # Cache backends (in-memory / Redis)
│   ├── routers/             # API route modules
│   ├── schemas/             # Request/response schemas
│   ├── services/            # Service layer package
│   ├── scrappers/           # Scraper package
│   └── utils/               # Shared utilities and scraping helpers
├── pyproject.toml           # Project metadata & dependencies
├── README.md
└── uv.lock                  # Dependency lockfile
```

## Caching

To avoid hammering the upstream source, endpoints should cache their results. A cache service is injected into any route via the `CacheDep` dependency, which exposes
two `async` methods:

- `get_from_cache(key)` — returns the cached value, or `None` if missing/expired.
- `add_to_cache(key, value, ttl)` — stores `value` under `key` for `ttl` seconds.

A typical "check cache, otherwise fetch and store" flow looks like this:

```python
from fastapi import APIRouter

from app.cache import CacheDep

router = APIRouter()


@router.get("/")
async def get_dolar(cache_store: CacheDep):
    # 1. Try the cache first.
    value = await cache_store.get_from_cache("dolar")
    if value is not None:
        return {"dolar": value}

    # 2. Cache miss: fetch the fresh value (e.g. from a service).
    value = await fetch_dolar_value()

    # 3. Store it so the next request is served from cache (ttl in seconds).
    await cache_store.add_to_cache("dolar", value, ttl=86400)
    return {"dolar": value}
```

> **Note:** the `ttl` is automatically capped so an entry never outlives the
> daily data reset (00:00 UTC-3), no matter how large a value you pass.


## How to Contribute

Want to add a new endpoint or improve an existing one? Great!

Check out our contribution guide in [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions.

When committing, follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary). 

## License

MIT license - See [LICENSE](LICENSE) for details.

---

Never used FastAPI before? Don't worry, it's a very accessible framework, and one of the best documented. You can learn the basics in the [official FastAPI documentation](https://fastapi.tiangolo.com/).
