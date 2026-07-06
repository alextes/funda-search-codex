# funda-search-codex

A personal house-search assistant for Funda listings.

The first proof of concept focuses on the riskiest part: getting structured data out of Funda reliably. It uses [`pyfunda`](https://github.com/0xMH/pyfunda), which talks to Funda's app-facing JSON APIs instead of scraping browser HTML.

## What It Does Now

- Searches Funda through `pyfunda`.
- Normalizes listings into a stable local shape.
- Computes price per square meter.
- Computes straight-line distance from central Amsterdam.
- Extracts neighborhood, coordinates, description, media, and floorplan URLs where available.
- Enriches search results with Funda detail data by default, because the search API is lighter and omits coordinates/floorplans.
- Tracks already-seen listing IDs in a local SQLite database.
- Writes a CSV and a simple private HTML overview.

## Setup

Use a virtual environment before installing Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Try The Proof Of Concept

```bash
source .venv/bin/activate
python -m funda_search fetch \
  --location amsterdam \
  --max-price 900000 \
  --min-area 60 \
  --pages 1 \
  --csv reports/amsterdam.csv \
  --html reports/amsterdam.html
```

By default this writes local state to `data/seen.sqlite`. The CSV includes an `is_new` column, so repeated runs can highlight houses that were not seen before.

Use `--skip-detail-enrichment` if you want a faster, lighter run that avoids fetching the detail page for each listing. That mode may not include coordinates or floorplans.

## Notes

`pyfunda` is unofficial and uses undocumented Funda APIs. It may break if Funda changes those APIs, and you should keep request volume modest. The dependency is AGPL-3.0 licensed, which matters if this project is distributed or hosted for others.

## Roadmap

See [ROADMAP.md](ROADMAP.md).
