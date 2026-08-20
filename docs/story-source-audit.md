# Story source audit — 20 August 2026

This audit separates verified source statements from proposed interpretation before the four-act rewrite.

## Frozen data checks

| Story point | Verified value | Source asset |
|---|---:|---|
| Samoa rainfall anomaly, 2020 | +27.3 mm (SE 1.5 mm) | `public/data/samoa-climate.json` from SPC/PDH `RAIN_ANOM` |
| Samoa rainfall anomaly, 2021 | −18.1 mm (SE 1.0 mm) | same |
| Samoa rainfall anomaly, 2022 | −20.7 mm (SE 0.8 mm) | same |
| Samoa EEZ SST anomaly, 2024 | +0.8°C (SE 0.1°C) | `public/data/samoa-climate.json` from SPC/PDH `SST_ANOM` |
| April 2016 near-Upolu rainfall | 522.3 mm; +358.47 mm from April normal | `public/data/seasonal-analysis.json` |
| February 1998 near-Upolu rainfall | 36.12 mm; −211.11 mm from February normal | `public/data/seasonal-analysis.json` |
| Taro yield, 1993 / 1994 / 2000 / 2024 | 3,409.1 / 1,500 / 5,000 / 5,574.6 kg/ha | `public/data/samoa-climate.json` from SPC/PDH taro yield |

April 2016 is the maximum positive monthly departure and February 1998 the minimum negative departure in the frozen 1981–2025 grid-point asset.

## Documentary checks

| Claim | Verification | Official source |
|---|---|---|
| Taro leaf blight devastated Samoa production in 1993. | Verified. The FAO paper states this directly and describes the narrow genetic base and subsequent programme. | https://www.fao.org/4/i2554e/i2554e00.pdf |
| The response involved regional genetic-resource exchange and farmer participation. | Verified. FAO documents introductions from Palau, FSM, the Philippines and later Asia; on-farm trials; farmer evaluation; and a participatory improvement programme involving farmers, researchers, USP, SPC and national staff. | same FAO paper |
| Samoa NDC 3.0 targets at least three climate-resilient crop varieties adapted to Samoa’s agro-ecological zones by 2035. | Verified. | https://www.mnre.gov.ws/wp-content/uploads/2026/01/Samoa-FINAL-NDC3.0_READYTOPRINT_10.12.2025.pdf |
| Adoption requires farmer consent. | Verified. NDC 3.0 says adoption would require consent from farmers and commercial and community-based farms. | same NDC |
| CIM plans enable each of Samoa’s 368 villages to identify locally relevant adaptation measures and leverage local knowledge. | Verified. | same NDC |

## Competition gates

The downloaded official 2026 rules state that entries must use at least one official Challenge dataset, cite all datasets, comply with licences, and use only open additional data. They allow supportive AI use but require the participant’s own original work and judgement. Interactive entries must remain accessible through 31 August 2029.

The rules also say entries must be created specifically for the Challenge and “neither previously published nor previously submitted elsewhere”. Because a public review URL already exists, the organiser should be asked in writing whether a clearly labelled work-in-progress preview affects eligibility. This audit does not resolve that ambiguity.

Source: https://pacificdatavizchallenge.org/sites/default/files/2026-05/Pacific-Dataviz-Challenge-2026-rules-reglement.pdf

## Publication decisions

- Mr Tom explicitly approved publishing the proposed Māori/Samoan family positionality statement in the Cloudflare review build on 20 August 2026.
- No family recollection of the 1993 taro crisis will be used without the speaker’s permission and attribution review.
- No additional Samoan or te reo Māori wording will be added without fluent-speaker review.
