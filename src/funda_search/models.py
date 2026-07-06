from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ListingSummary:
    id: str
    title: str | None
    city: str | None
    neighborhood: str | None
    price: int | None
    living_area_m2: int | None
    price_per_m2: float | None
    rooms: int | None
    bedrooms: int | None
    energy_label: str | None
    latitude: float | None
    longitude: float | None
    distance_to_amsterdam_center_km: float | None
    publication_date: str | None
    url: str | None
    floorplan_urls: list[str]
    description: str | None
    description_matches: list[str]
    is_new: bool = True

    def with_seen_status(self, is_new: bool) -> "ListingSummary":
        return replace(self, is_new=is_new)

    def to_row(self) -> dict[str, object]:
        return {
            "is_new": self.is_new,
            "id": self.id,
            "title": self.title,
            "city": self.city,
            "neighborhood": self.neighborhood,
            "price": self.price,
            "living_area_m2": self.living_area_m2,
            "price_per_m2": round(self.price_per_m2) if self.price_per_m2 is not None else None,
            "rooms": self.rooms,
            "bedrooms": self.bedrooms,
            "energy_label": self.energy_label,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "distance_to_amsterdam_center_km": (
                round(self.distance_to_amsterdam_center_km, 1)
                if self.distance_to_amsterdam_center_km is not None
                else None
            ),
            "publication_date": self.publication_date,
            "url": self.url,
            "floorplan_urls": " ".join(self.floorplan_urls),
            "description_matches": ", ".join(self.description_matches),
        }
