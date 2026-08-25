# Reproducibility and source record

This repository contains the interactive entry **When Water Changes, Everything Changes** for the Pacific DataViz Challenge 2026.

## Run the entry

```sh
npm install
python3 scripts/check_data.py
npm run build
npm run test
```

The deployed entry is intended to remain available at:

https://pdc-samoa-climate-preview.pages.dev/

through 31 August 2029.

## Data record

| Rendered material | Publisher and dataset | Geography, period and unit | Accessed | Transformation | Frozen material in this repository |
| --- | --- | --- | --- | --- | --- |
| Annual rainfall anomaly | Pacific Community (SPC), Pacific Data Hub .Stat, `DF_CLIMATE_CHANGE` / `RAIN_ANOM` | Samoa-wide annual anomaly, 1979–2025, mm; 1991–2020 baseline | 2026-08-17 | Retained as published; chart highlights 2020–2022 only | `public/data/samoa-climate.json` |
| Annual sea-surface-temperature anomaly | Pacific Community (SPC), Pacific Data Hub .Stat, `DF_CLIMATE_CHANGE` / `SST_ANOM` | Samoa EEZ aggregate, annual, 1979–2025, °C; 1971–2000 baseline | 2026-08-17 | Retained as published | `public/data/samoa-climate.json` |
| Taro yield | Pacific Community (SPC), Pacific Data Hub .Stat, `DF_AGRICULTURAL_PRODUCTION` / `TARO.CROP_YIELD` | Samoa country-level annual yield, 1961–2024, kg/ha | 2026-08-17 | Retained as published | `data/raw/spc-samoa-taro-yield.csv`, `public/data/samoa-climate.json` |
| Monthly precipitation illustration | NASA POWER API `PRECTOTCORR`, source response identified as MERRA-2 | Grid cell at −13.83°, −171.75°; monthly, 1981–2025 | 2026-08-18 | Mean daily precipitation in mm multiplied by days in the calendar month; departures calculated against each month’s 1981–2025 record mean | `data/raw/nasa-power-upolu-monthly-precipitation-1981-2025.json`, `data/processed/nasa-power-upolu-monthly-precipitation-1981-2025.csv`, `public/data/seasonal-analysis.json` |
| Niño 3.4 appendix context | NOAA Physical Sciences Laboratory | Monthly Niño 3.4 SST | 2026-08-18 | Converted locally to 1981–2010 calendar-month anomalies | `data/raw/noaa-psl-nino34-monthly.data`, `public/data/seasonal-analysis.json` |

The retained NASA POWER response records API version `v2.9.7`.

## Source links

- [SPC/Pacific Data Hub rainfall anomaly](https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions)
- [SPC/Pacific Data Hub EEZ SST anomaly](https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions)
- [SPC/Pacific Data Hub Samoa taro yield](https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS.TARO.CROP_YIELD?dimensionAtObservation=AllDimensions)
- [NASA POWER API request](https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=PRECTOTCORR&community=AG&longitude=-171.75&latitude=-13.83&start=1981&end=2025&format=JSON)
- [NASA POWER referencing guide](https://power.larc.nasa.gov/docs/referencing/)
- [NOAA PSL Niño 3.4 source](https://psl.noaa.gov/data/correlation/nina34.data)
- [FAO: The taro improvement programme in Samoa](https://www.fao.org/4/i2554e/i2554e00.pdf)
- [Samoa NDC 3.0](https://www.mnre.gov.ws/wp-content/uploads/2026/01/Samoa-FINAL-NDC3.0_READYTOPRINT_10.12.2025.pdf)

## Licence and reuse status

Pacific Data Hub states that each dataset carries its own applicable licence and that users must follow that dataset-specific licence and attribution requirement. The exact dataset-page licence terms for the SPC indicators above have **not yet been independently verified**. Do not treat this repository or entry as cleared for final submission until those terms are confirmed and recorded.

Source: [Pacific Data Hub terms of use](https://pacificdata.org/terms-use).

## Authorship and AI assistance

The entrant conceived the question, selected the datasets and transformations, interpreted the results, and made the cultural, narrative and visual-design decisions. AI-assisted work was limited to coding support, debugging, accessibility checks and wording alternatives. The entrant retains final editorial and submission responsibility.
