from __future__ import annotations

import csv
import html
from pathlib import Path

from .models import ListingSummary

CSV_FIELDS = [
    "is_new",
    "id",
    "title",
    "city",
    "neighborhood",
    "price",
    "living_area_m2",
    "price_per_m2",
    "rooms",
    "bedrooms",
    "energy_label",
    "distance_to_amsterdam_center_km",
    "publication_date",
    "url",
    "floorplan_urls",
    "description_matches",
]


def write_csv(path: Path, listings: list[ListingSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for listing in listings:
            row = listing.to_row()
            writer.writerow({field: row.get(field) for field in CSV_FIELDS})


def write_html(path: Path, listings: list[ListingSummary], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(_listing_card(listing) for listing in listings)
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17201b;
      --muted: #58635d;
      --line: #d9dfdb;
      --surface: #f7f8f5;
      --accent: #1a7352;
      --new: #b93d24;
    }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: white;
    }}
    header {{
      padding: 28px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: var(--surface);
    }}
    h1 {{
      margin: 0;
      font-size: 28px;
      letter-spacing: 0;
    }}
    main {{
      padding: 20px 32px 40px;
      display: grid;
      gap: 14px;
    }}
    article {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      display: grid;
      gap: 12px;
    }}
    article.new {{
      border-color: color-mix(in srgb, var(--new) 45%, var(--line));
    }}
    .topline {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
    }}
    h2 {{
      margin: 0;
      font-size: 18px;
      letter-spacing: 0;
    }}
    a {{
      color: var(--accent);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}
    .badge {{
      color: var(--new);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    dl {{
      margin: 0;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px 16px;
    }}
    dt {{
      color: var(--muted);
      font-size: 12px;
    }}
    dd {{
      margin: 3px 0 0;
      font-weight: 650;
    }}
    p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.45;
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    @media (max-width: 680px) {{
      header, main {{
        padding-left: 16px;
        padding-right: 16px;
      }}
      .topline {{
        display: grid;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <p>{len(listings)} listings in this export.</p>
  </header>
  <main>
    {rows or "<p>No listings to show.</p>"}
  </main>
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")


def _listing_card(listing: ListingSummary) -> str:
    description = html.escape(_shorten(listing.description or "", 420))
    floorplans = " ".join(
        f'<a href="{html.escape(url)}">Floorplan {index}</a>'
        for index, url in enumerate(listing.floorplan_urls, start=1)
    )
    matches = ", ".join(listing.description_matches) if listing.description_matches else "none"
    return f"""<article class="{'new' if listing.is_new else ''}">
  <div class="topline">
    <h2><a href="{html.escape(listing.url or '#')}">{html.escape(listing.title or 'Untitled listing')}</a></h2>
    {'<span class="badge">New</span>' if listing.is_new else ''}
  </div>
  <dl>
    <div><dt>Price</dt><dd>{_money(listing.price)}</dd></div>
    <div><dt>Price / m2</dt><dd>{_money(listing.price_per_m2)}</dd></div>
    <div><dt>Area</dt><dd>{_value(listing.living_area_m2, 'm2')}</dd></div>
    <div><dt>Neighborhood</dt><dd>{html.escape(listing.neighborhood or listing.city or 'unknown')}</dd></div>
    <div><dt>Center distance</dt><dd>{_km(listing.distance_to_amsterdam_center_km)}</dd></div>
    <div><dt>Rooms</dt><dd>{_value(listing.rooms)}</dd></div>
    <div><dt>Bedrooms</dt><dd>{_value(listing.bedrooms)}</dd></div>
    <div><dt>Energy</dt><dd>{html.escape(listing.energy_label or 'unknown')}</dd></div>
  </dl>
  <p>{description}</p>
  <p>Description matches: {html.escape(matches)}</p>
  <div class="links">{floorplans or '<span>No floorplan URL found</span>'}</div>
</article>"""


def _money(value: float | int | None) -> str:
    if value is None:
        return "unknown"
    return f"EUR {value:,.0f}"


def _km(value: float | None) -> str:
    if value is None:
        return "unknown"
    return f"{value:.1f} km"


def _value(value: object, suffix: str = "") -> str:
    if value is None:
        return "unknown"
    return f"{value} {suffix}".strip()


def _shorten(value: str, max_length: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 1].rstrip() + "..."
