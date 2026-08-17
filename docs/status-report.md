# Framework status report — 17 August 2026

## Completed
- Created a local Astro + TypeScript static framework.
- Added client-side Observable Plot charts for observed Samoa annual rainfall anomalies and SST anomalies.
- Added an evidence manifest, data-quality script and analysis-notebook scaffold.
- Added Playwright smoke test and print/PDF renderer.
- Generated draft PDF and full-page PNG artefacts.
- Updated WordPress page 219 after authenticated preflight. It remains **draft** and is not publicly published.

## Verified execution
- `python3 scripts/check_data.py`: PASS — rainfall and SST each contain 47 contiguous annual observations (1979–2025).
- `npm run build`: PASS — Astro static build completed.
- `npm run test`: PASS — 1 Playwright test passed.
- `npm run render:pdf`: PASS — `artifacts/draft-framework.pdf` and `artifacts/draft-framework.png` created.

## Source-backed data currently rendered
- SPC Pacific Data Hub annual Samoa rainfall anomaly (`RAIN_ANOM`), national aggregate.
- SPC Pacific Data Hub annual Samoa SST anomaly (`SST_ANOM`), EEZ aggregate.

See `evidence-manifest.md` for SDMX URLs, baselines and limitations.

## Held deliberately for later
- Crop selection and food-resilience evidence.
- Population and water-service indicators.
- Any station/catchment/community data.
- Seasonal outlook or long-run scenario layers.
- Any causal, risk-ranking or operational forecast claim.
- Public hosting or publication.

## Additional source audit integrated
- Corrected the rainfall wording: inspected metadata identifies a Samoa-wide series but does **not** state its station/grid/national-area aggregation method.
- Added data catalogue/reuse notes: PDH labels the datasets `Other (Open)`, but a specific licence text/URL was not displayed; attribution is required and additional reuse terms remain unverified.
- Recorded exact held-source endpoints for 22 crop items, estimated/projected population growth, the dated Samoa Meteorology seasonal outlook, Samoa NDC 3.0 and the World Bank country profile.
- Added explicit in-chart labels: **exploratory annual-data view — not a forecast or causal estimate**.

## WordPress verification
Authenticated preflight succeeded. Page 219 was read before and after the write; status remained `draft`, title remained `Pacific Dataviz Challenge 2026 — Draft`, and content read-back matched the submitted draft content.

## Decisions needed later
1. Confirm whether to pursue authorised Samoa station/seasonal-outlook data.
2. Select a crop only after provenance and local relevance review.
3. Approve a durable public static-hosting path before any deployment.
