# When Water Changes, Everything Changes

An interactive Pacific DataViz Challenge 2026 story about Samoa’s rainfall variability, water and planning.

## Scope

The story uses annual Samoa-wide rainfall anomalies, Samoa EEZ sea-surface-temperature anomalies, country-level taro yield, and a separate coarse near-Upolu MERRA-2/POWER monthly illustration. These sources retain distinct spatial scopes, units and baselines. The story does not make an operational forecast, causal estimate or local risk ranking.

## Run

```sh
npm install
python3 scripts/build_spc_climate.py
python3 scripts/check_data.py
node scripts/build_seasonal_analysis.mjs
npm run dev
npm run build
npm run test
```

## Structure

- `public/data/`: published, source-derived web data
- `data/raw/`: retained raw source captures and checksums
- `scripts/build_spc_climate.py`: deterministic SPC-capture transformation
- `docs/evidence-manifest.md`: evidence ledger and scope limits
- `docs/licence-matrix.md`: licence/attribution record and outstanding confirmation
- `docs/story-source-audit.md`: source checks and competition gates
- `src/pages/index.astro`: interactive story
- `tests/`: Playwright coverage

## Data, licensing and submission gates

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md), [`docs/evidence-manifest.md`](docs/evidence-manifest.md), and [`docs/licence-matrix.md`](docs/licence-matrix.md). The public Pacific Data Hub records inspected for the SPC indicators do not expose their dataset-specific reuse terms. The entry is not represented as cleared for final submission until SPC confirms those terms. The competition organiser should also confirm that the public preview and repository satisfy its publication rule.

## Development documentation

- Astro: https://docs.astro.build/en/install-and-setup/
- Observable Plot: https://observablehq.com/plot/getting-started
- MapLibre GL JS: https://maplibre.org/maplibre-gl-js/docs/
- Playwright: https://playwright.dev/docs/test-intro
