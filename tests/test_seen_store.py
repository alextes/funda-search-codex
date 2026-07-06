from __future__ import annotations

from funda_search.models import ListingSummary
from funda_search.seen_store import SeenStore


def test_seen_store_marks_new_then_seen(tmp_path) -> None:
    listing = ListingSummary(
        id="abc",
        title="Test",
        city=None,
        neighborhood=None,
        price=None,
        living_area_m2=None,
        price_per_m2=None,
        rooms=None,
        bedrooms=None,
        energy_label=None,
        latitude=None,
        longitude=None,
        distance_to_amsterdam_center_km=None,
        publication_date=None,
        url=None,
        floorplan_urls=[],
        description=None,
        description_matches=[],
    )

    with SeenStore(tmp_path / "seen.sqlite") as store:
        first = store.mark_and_record([listing])
        second = store.mark_and_record([listing])

    assert first[0].is_new is True
    assert second[0].is_new is False
