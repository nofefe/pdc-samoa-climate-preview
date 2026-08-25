# The Year We Plan For — framework

Draft-only framework for a Pacific Dataviz Challenge 2026 interactive story about Samoa's observed rainfall variability and sea-surface-temperature context.

## Status
**Framework, not submission.** No operational forecast, causal claim, local risk ranking or publication is included.

## Run

```sh
npm install
python3 scripts/check_data.py
npm run dev
npm run build
```

## Test and produce draft print artefacts

```sh
npm run test
npm run render:pdf
```

## Structure
- `public/data/`: source-derived framework data
- `docs/evidence-manifest.md`: source ledger, caveats and held evidence gates
- `scripts/check_data.py`: structural data checks
- `src/pages/index.astro`: initial visual story
- `tests/`: Playwright smoke test and print artefact generation

## Data and interpretation
See [`docs/evidence-manifest.md`](docs/evidence-manifest.md) and [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md). The site shows annual national rainfall anomalies and Samoa-EEZ SST anomalies. They use different baselines and must not be interpreted as local observations or causal evidence.

## Framework documentation sources
- Astro: https://docs.astro.build/en/install-and-setup/
- Observable Plot: https://observablehq.com/plot/getting-started
- MapLibre GL JS: https://maplibre.org/maplibre-gl-js/docs/
- Playwright: https://playwright.dev/docs/test-intro
