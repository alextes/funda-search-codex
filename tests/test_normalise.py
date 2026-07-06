from __future__ import annotations

from types import SimpleNamespace

from funda_search.normalise import normalise_listing


def test_normalise_listing_computes_core_fields() -> None:
    listing = SimpleNamespace(
        global_id=123,
        title="Nice apartment",
        city="Amsterdam",
        price=SimpleNamespace(amount=600000),
        living_area=75,
        rooms_count=3,
        bedrooms=2,
        energy_label="A3",
        publication_date="2026-07-06",
        url="https://www.funda.nl/detail/koop/amsterdam/test/123/",
        description="Eigen grond, actieve VvE en een balkon.",
        address=SimpleNamespace(neighbourhood="Oud-West", city="Amsterdam"),
        location=SimpleNamespace(latitude=52.3676, longitude=4.9041),
        media=SimpleNamespace(
            floorplans=[
                SimpleNamespace(url="https://example.com/floorplan/{index}/"),
                SimpleNamespace(url="https://example.com/floorplan/{index}/"),
            ]
        ),
    )

    summary = normalise_listing(listing)

    assert summary.id == "123"
    assert summary.price_per_m2 == 8000
    assert summary.neighborhood == "Oud-West"
    assert summary.distance_to_amsterdam_center_km == 0
    assert summary.energy_label == "A+++"
    assert summary.floorplan_urls == [
        "https://example.com/floorplan/1/",
        "https://example.com/floorplan/2/",
    ]
    assert summary.description_matches == ["eigen grond", "vve", "balkon"]


def test_normalise_listing_handles_missing_values() -> None:
    listing = SimpleNamespace(id="missing", title=None)

    summary = normalise_listing(listing)

    assert summary.id == "missing"
    assert summary.price is None
    assert summary.price_per_m2 is None
    assert summary.floorplan_urls == []
