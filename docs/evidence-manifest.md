# Evidence manifest — framework stage

## Scope
This is a draft framework, not a final competition entry or operational climate service. Values shown are observed annual aggregates from the official Challenge data catalogue. The app deliberately does not forecast water-system failure, disaster impacts or crop yields.

## Initial rendered data

| Dataset | Source / access URL | Framework use | Actual Samoa coverage | Spatial basis, baseline and limitations |
|---|---|---|---|---|
| Precipitation anomalies (`RAIN_ANOM`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions | Hero variability chart | 1979–2025; annual; mm; 47 rows; standard-error field | Samoa-wide series. Annual total precipitation minus the 1991–2020 average annual total. The inspected metadata does not specify station/grid/national-area aggregation; not local/station evidence. |
| Mean sea-surface-temperature anomalies (`SST_ANOM`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions | Long-run climate-context chart | Full official Samoa record: 1850–2025; framework view: 1979–2025; annual; °C | Samoa EEZ annual mean. Anomaly baseline: 1971–2000. Not a coastal/inshore or land temperature series; raw magnitudes are not comparable with rainfall anomalies. |
| Challenge rules/data catalogue | https://pacificdatavizchallenge.org/ | Eligibility/data-list check | 2026 | Recheck immediately before submission. |

## Verified, held for the next evidence gate

| Dataset / source | Exact public access URL | Verified use and limitation |
|---|---|---|
| **Taro yield** (`TARO`, `CROP_YIELD`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS.TARO.CROP_YIELD?dimensionAtObservation=AllDimensions | **Rendered in Draft 0.2.** Samoa annual country-level context, 1961–2024, kg/ha; 64 contiguous observations. Raw response retained at `data/raw/spc-samoa-taro-yield.csv`, acquired by `scripts/fetch_taro.py`. It is descriptive only: do not infer climate caused yield outcomes or forecast yield. |
| Other disaggregated crop yields | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS..CROP_YIELD?dimensionAtObservation=AllDimensions | Samoa national, 22 crop items, 1961–2024, kg/ha. Held pending item definition, provenance and local-relevance review. |
| Headline crop yield | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.CROP_YIELD.WS?dimensionAtObservation=AllDimensions | Samoa annual aggregate, 1961–2024, kg/ha. Do not treat as an individual crop or assume undocumented aggregation/weighting. |
| Total population growth (`NMDI0002`) | https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_NMDI_POP,1.0/A.WS.NMDI0002._T._T._T._T._Z?dimensionAtObservation=AllDimensions | Samoa annual 1990–2025, percent. All returned observations are `E`, sourced as PDH.Stat population projections; do not label it observed census change. |
| Samoa Meteorology Division El Niño Update No. 2 (11 Aug 2026) | https://www.mnre.gov.ws/wp-content/uploads/2026/08/FINAL-El-Nino-Update-No.2-11082026-final.pdf | Possible dated Aug 2026–Jan 2027 Samoa-wide seasonal-outlook panel. It reports probabilities, not local forecasts or observed impact. Attribute MNRE/Samoa Meteorology Division; no reuse licence was identified. |
| Samoa NDC 3.0 (Oct 2025) | https://unfccc.int/sites/default/files/2026-01/Samoa%20NDC3.0_FINAL.pdf | National policy/decsion context to 2035. It is a commitment, not a local climate data source or proof of outcomes. |
| World Bank Climate Risk Country Profile: Samoa (2021) | https://climateknowledgeportal.worldbank.org/sites/default/files/country-profiles/15821-WB_Samoa%20Country%20Profile-WEB.pdf | Scenario/model-ensemble context only; CMIP5/RCP vintage and limited small-scale reliability must be shown. |

## Catalogue and reuse notes
The public PDH catalogue lists the inspected datasets as **Other (Open)** but does not show a specific licence URL/text. The Pacific Data Hub Terms of Use require users to comply with a dataset's specific licence and attribute the data custodian. Reuse terms beyond attribution are therefore not fully verified. Attribute: **Pacific Community (SPC), Statistics for Development Division / Pacific Data Hub .Stat; relevant dataflow and access date.**

Metadata endpoints:
- Climate dataflow: https://stats-sdmx-disseminate.pacificdata.org/rest/dataflow/SPC/DF_CLIMATE_CHANGE/1.0?references=all&detail=referencepartial
- Agriculture dataflow: https://stats-sdmx-disseminate.pacificdata.org/rest/dataflow/SPC/DF_AGRICULTURAL_PRODUCTION/1.0?references=all&detail=referencepartial
- Population dataflow: https://stats-sdmx-disseminate.pacificdata.org/rest/dataflow/SPC/DF_NMDI_POP/1.0?references=all&detail=referencepartial

## Method guardrails
- Taro is the selected opening crop because SPC describes it as Samoa’s most commonly grown root crop and preferred starchy staple. SPC’s figures on households, plantings and exports are 2014–15 historical context, not a current estimate: https://pafpnet.spc.int/policy-bank/countries/samoa. An FAO Samoa study documents that taro leaf blight devastated taro in 1993; this history is used as context, not as a statistical attribution from the series: https://www.fao.org/4/y8345e/y8345e03.htm
- The taro yield series is a country-level annual agricultural measure. The framework does not align it with rainfall or SST in one chart, calculate correlation, infer a cause, or generate a forecast.
- The initial shared annual comparison window is 1979–2025 for rainfall and SST; the rainfall–SST–taro overlap is 1979–2024. A shared time window does not establish a relationship.
- No causal attribution between displayed series.
- No trend claim for rainfall in this framework.
- Positive or negative anomaly means relative to each series' own baseline; values are not combined.
- Missing values remain missing.
- Future population scenarios, seasonal outlooks and climate projections must be visually and structurally separate from observations.
- Suppress rather than fabricate an output where unit, geography, overlap, quality metadata or minimum sample size is inadequate.
