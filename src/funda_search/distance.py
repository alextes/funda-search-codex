from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

AMSTERDAM_CENTER = (52.3676, 4.9041)
EARTH_RADIUS_KM = 6371.0088


def distance_km(
    latitude: float | None,
    longitude: float | None,
    origin: tuple[float, float] = AMSTERDAM_CENTER,
) -> float | None:
    if latitude is None or longitude is None:
        return None

    origin_latitude, origin_longitude = origin
    lat1 = radians(origin_latitude)
    lon1 = radians(origin_longitude)
    lat2 = radians(latitude)
    lon2 = radians(longitude)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))
