from __future__ import annotations

import argparse
from pathlib import Path

from .export import write_csv, write_html
from .pyfunda_source import fetch_listings
from .seen_store import SeenStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="funda-search",
        description="Fetch Funda listings and write a focused house-search overview.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch = subparsers.add_parser("fetch", help="Fetch listings from Funda")
    fetch.add_argument("--location", default="amsterdam", help="City, postcode, or Funda area id")
    fetch.add_argument("--category", default="buy", choices=["buy", "rent", "sold"])
    fetch.add_argument("--min-price", type=int)
    fetch.add_argument("--max-price", type=int)
    fetch.add_argument("--min-area", type=int)
    fetch.add_argument("--max-area", type=int)
    fetch.add_argument("--min-rooms", type=int)
    fetch.add_argument("--min-bedrooms", type=int)
    fetch.add_argument("--radius-km", type=int)
    fetch.add_argument("--sort", default="newest")
    fetch.add_argument("--pages", type=int, default=1, help="Number of search pages to fetch")
    fetch.add_argument("--workers", type=int, default=1, help="Parallel page workers when pages > 1")
    fetch.add_argument(
        "--skip-detail-enrichment",
        action="store_true",
        help="Only use search-result data. Faster, but usually misses coordinates and floorplans.",
    )
    fetch.add_argument("--state", type=Path, default=Path("data/seen.sqlite"))
    fetch.add_argument("--csv", type=Path, default=Path("reports/listings.csv"))
    fetch.add_argument("--html", type=Path, default=Path("reports/listings.html"))
    fetch.add_argument(
        "--include-seen",
        action="store_true",
        help="Include listings that were already seen in earlier runs",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "fetch":
        filters = {
            "category": args.category,
            "min_price": args.min_price,
            "max_price": args.max_price,
            "min_area": args.min_area,
            "max_area": args.max_area,
            "min_rooms": args.min_rooms,
            "min_bedrooms": args.min_bedrooms,
            "radius_km": args.radius_km,
            "sort": args.sort,
        }
        filters = {key: value for key, value in filters.items() if value is not None}

        listings = fetch_listings(
            location=args.location,
            max_pages=args.pages,
            workers=args.workers,
            filters=filters,
            enrich_details=not args.skip_detail_enrichment,
        )

        with SeenStore(args.state) as store:
            annotated = store.mark_and_record(listings)

        if not args.include_seen:
            annotated = [listing for listing in annotated if listing.is_new]

        write_csv(args.csv, annotated)
        write_html(args.html, annotated, title=f"Funda listings for {args.location}")

        print(f"Fetched {len(listings)} listings.")
        print(f"Wrote {len(annotated)} listings to {args.csv} and {args.html}.")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
