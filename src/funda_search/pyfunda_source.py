from __future__ import annotations

from collections.abc import Iterator

from .models import ListingSummary
from .normalise import normalise_listing


def fetch_listings(
    location: str,
    max_pages: int,
    workers: int,
    filters: dict[str, object],
    enrich_details: bool = True,
) -> list[ListingSummary]:
    try:
        from funda import Funda
    except ImportError as exc:
        raise SystemExit(
            "pyfunda is not installed. Create a venv and run: "
            'python -m pip install -e ".[dev]"'
        ) from exc

    with Funda() as client:
        raw_listings = list(
            _iter_raw_listings(
                client=client,
                location=location,
                max_pages=max_pages,
                workers=workers,
                filters=filters,
            )
        )
        if enrich_details:
            raw_listings = _enrich_detail_listings(client, raw_listings)
        return [normalise_listing(listing) for listing in raw_listings]


def _enrich_detail_listings(client: object, listings: list[object]) -> list[object]:
    enriched: list[object] = []
    for listing in listings:
        try:
            enriched.append(client.listing(_listing_reference(listing)))
        except Exception as exc:  # noqa: BLE001 - keep partial reports useful when one detail call fails.
            print(f"Warning: detail enrichment failed for {_listing_reference(listing)}: {exc}")
            enriched.append(listing)
    return enriched


def _listing_reference(listing: object) -> object:
    return (
        getattr(listing, "url", None)
        or getattr(listing, "global_id", None)
        or getattr(listing, "id", None)
        or listing
    )


def _iter_raw_listings(
    client: object,
    location: str,
    max_pages: int,
    workers: int,
    filters: dict[str, object],
) -> Iterator[object]:
    if max_pages <= 1:
        yield from client.search(location, **filters)
        return

    yield from client.iter_search(
        location,
        max_pages=max_pages,
        workers=workers,
        **filters,
    )
