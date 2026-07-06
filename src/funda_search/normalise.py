from __future__ import annotations

from collections.abc import Iterable

from .distance import distance_km
from .models import ListingSummary

DESCRIPTION_KEYWORDS = [
    "erfpacht",
    "eigen grond",
    "fundering",
    "vve",
    "renovatie",
    "kluswoning",
    "balkon",
    "dakterras",
    "tuin",
    "parkeer",
    "energielabel",
]


def normalise_listing(listing: object) -> ListingSummary:
    price = _nested_attr(listing, "price", "amount")
    living_area = _first_present(
        _attr(listing, "living_area"),
        _nested_attr(listing, "areas", "living_area"),
        _nested_attr(listing, "areas", "usable_area"),
    )
    latitude = _first_present(
        _nested_attr(listing, "location", "latitude"),
        _nested_attr(listing, "location", "coordinates", "latitude"),
    )
    longitude = _first_present(
        _nested_attr(listing, "location", "longitude"),
        _nested_attr(listing, "location", "coordinates", "longitude"),
    )
    description = _attr(listing, "description")
    listing_id = _first_present(
        _attr(listing, "global_id"),
        _attr(listing, "id"),
        _attr(listing, "tiny_id"),
        _attr(listing, "url"),
    )

    return ListingSummary(
        id=str(listing_id),
        title=_attr(listing, "title"),
        city=_first_present(_attr(listing, "city"), _nested_attr(listing, "address", "city")),
        neighborhood=_nested_attr(listing, "address", "neighbourhood"),
        price=_as_int(price),
        living_area_m2=_as_int(living_area),
        price_per_m2=_price_per_m2(price, living_area),
        rooms=_first_present(_attr(listing, "rooms_count"), _nested_attr(listing, "rooms", "total")),
        bedrooms=_attr(listing, "bedrooms"),
        energy_label=_energy_label(_attr(listing, "energy_label")),
        latitude=_as_float(latitude),
        longitude=_as_float(longitude),
        distance_to_amsterdam_center_km=distance_km(_as_float(latitude), _as_float(longitude)),
        publication_date=str(_attr(listing, "publication_date") or ""),
        url=_first_present(_attr(listing, "url"), _attr(listing, "detail_url")),
        floorplan_urls=_media_urls(_nested_attr(listing, "media", "floorplans")),
        description=description,
        description_matches=_description_matches(description),
    )


def _price_per_m2(price: object, living_area: object) -> float | None:
    price_value = _as_float(price)
    area_value = _as_float(living_area)
    if price_value is None or area_value is None or area_value <= 0:
        return None
    return price_value / area_value


def _description_matches(description: str | None) -> list[str]:
    if not description:
        return []
    lower = description.lower()
    return [keyword for keyword in DESCRIPTION_KEYWORDS if keyword in lower]


def _media_urls(items: object) -> list[str]:
    if not items:
        return []
    if isinstance(items, str):
        return [items]
    if not isinstance(items, Iterable):
        return []

    urls: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(items, start=1):
        value = _first_present(
            _attr(item, "url"),
            _attr(item, "href"),
            _attr(item, "original"),
            _attr(item, "large"),
            item if isinstance(item, str) else None,
        )
        if value:
            url = str(value).replace("{index}", str(index))
            if url not in seen:
                urls.append(url)
                seen.add(url)
    return urls


def _energy_label(value: object) -> str | None:
    if value is None or value == "":
        return None
    label = str(value)
    return {
        "A1": "A+",
        "A2": "A++",
        "A3": "A+++",
        "A4": "A++++",
    }.get(label, label)


def _nested_attr(value: object, *names: str) -> object | None:
    current = value
    for name in names:
        current = _attr(current, name)
        if current is None:
            return None
    return current


def _attr(value: object, name: str) -> object | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)


def _first_present(*values: object) -> object | None:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _as_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: object) -> int | None:
    float_value = _as_float(value)
    if float_value is None:
        return None
    return int(float_value)
