# Roadmap

## Proof Of Concept

- [x] Create a local Python project.
- [x] Try `pyfunda` as the first data source.
- [x] Normalize listings into CSV and HTML.
- [x] Track seen listings across runs.
- [x] Compute price per square meter.
- [x] Compute straight-line distance from central Amsterdam.
- [x] Surface neighborhood and floorplan URLs.
- [ ] Run the proof of concept against live Funda data.
- [ ] Push the repo to GitHub.

## Search Workflow

- [ ] Add saved search profiles for different target areas and budgets.
- [ ] Schedule a daily morning run.
- [ ] Highlight newly discovered homes since the previous run.
- [ ] Keep a local archive of listing detail snapshots.
- [ ] Deduplicate listings across overlapping searches.

## Analysis

- [ ] Score descriptions for recurring preferences.
- [ ] Detect renovation risk, leasehold mentions, VvE details, foundation notes, outdoor space, and parking.
- [ ] Extract and display floorplans more prominently.
- [ ] Add travel-time estimates instead of only straight-line distance.
- [ ] Add neighborhood labels beyond Funda's own neighborhood field.
- [ ] Track price changes and listing age.

## Interface

- [ ] Improve the HTML report into a private local web app.
- [ ] Add filters, sorting, and favorite/reject status.
- [ ] Add notes per listing.
- [ ] Add spreadsheet export.
- [ ] Add map view.

## Data Source Fallbacks

- [ ] Inspect raw `pyfunda` payloads for missing fields.
- [ ] Add polite HTML scraping fallback if `pyfunda` misses fields.
- [ ] Add browser-assisted extraction fallback for cases where HTML scraping is blocked.
