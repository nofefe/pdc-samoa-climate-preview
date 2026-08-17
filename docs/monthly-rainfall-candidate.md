# Monthly rainfall candidate — NASA/POWER grid point near central Upolu

## Status

**Candidate for the proposed monthly taro-leaf seasonal calendar; not yet incorporated into the entry.**

## Capture

- Endpoint: `https://power.larc.nasa.gov/api/temporal/monthly/point`
- Parameter: `PRECTOTCORR` (*Precipitation Corrected*), supplied as mean daily precipitation in `mm/day`.
- API response source: `MERRA2`.
- Time coverage retrieved: January 1981–December 2025 (540 month records).
- Selected grid-point request: latitude `-13.83`, longitude `-171.75`.
- Raw response: `data/raw/nasa-power-upolu-monthly-precipitation-1981-2025.json`.
- Derived table: `data/processed/nasa-power-upolu-monthly-precipitation-1981-2025.csv`.
- Reproduction: `python3 scripts/fetch_nasa_power_rainfall.py`.

## Transformation

The source value remains in `mean_daily_precipitation_mm`. The derived monthly-total column is:

`mean_daily_precipitation_mm × calendar days in that month`

No missing source values were converted to zero. The retrieval produced 45 observations for each calendar month.

## Interpretation boundaries

This is a **NASA/POWER MERRA-2 gridded product at the requested coordinate**, not a Samoa-wide observation series, a named weather-station record, a village estimate or a water-system measurement. If used, the chart must be titled and labelled accordingly — for example:

> Monthly precipitation distribution at a NASA/POWER grid point near central Upolu, 1981–2025.

It may support a seasonal-variability display, but must not be merged with the SPC Samoa-wide annual anomaly series, used to infer household water security, or presented as a local rainfall forecast.

## Why retained

Unlike the current SPC `RAIN_ANOM` dataset, whose inspected dataflow contains annual Samoa-wide anomalies only, this capture has the monthly historical values needed to calculate month-specific distributions. It is a secondary contextual product; the existing official SPC annual series remains the Challenge-data foundation.
