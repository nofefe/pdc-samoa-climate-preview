# Evidence manifest — framework stage

## Scope
This is a draft framework, not a final competition entry or operational climate service. Values shown are observed annual aggregates from the official Challenge data catalogue. The app deliberately does not forecast water-system failure, disaster impacts or crop yields.

## Sources in the initial prototype

| Dataset | Source / access URL | Framework use | Coverage used | Limitations |
|---|---|---|---|---|
| Precipitation anomalies (`RAIN_ANOM`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions | Hero variability chart | 1979–2025, annual | National aggregate; anomaly baseline is 1991–2020; includes standard error; not village/station data. |
| Mean sea-surface-temperature anomalies (`SST_ANOM`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions | Long-run climate-context chart | 1979–2025 shown (full official series extends earlier) | Samoa EEZ aggregate; anomaly baseline is 1971–2000; not an inshore/coastal observation. |
| Challenge rules/data catalogue | https://pacificdatavizchallenge.org/ | Eligibility/data-list check | 2026 | Recheck immediately before submission. |

## Held for later evidence gate
- Disaggregated crop yields: add only after exact item choice, provenance and interpretation are checked.
- Population growth: PDH.Stat series is flagged estimated/projection; do not use as observed population without disclosure.
- Seasonal outlook: add only with an authoritative provider, dated product and documented hindcast skill.
- Station, catchment, water and local knowledge: require an authorised source, quality metadata and/or informed consent.
- Climate projection ensembles: use published scenario data only and label projections, never forecasts.

## Method guardrails
- No causal attribution between the two displayed series.
- No trend claim for rainfall in this framework.
- Positive or negative anomaly means relative to each series' own baseline; values are not combined.
- Missing values remain missing.
