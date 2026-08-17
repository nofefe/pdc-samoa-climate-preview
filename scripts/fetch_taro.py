"""Retrieve the official Samoa taro-yield series and update the local web data asset.

This is a reproducible acquisition step, not a model. The resulting yield series is
Samoa-wide annual context and must not be interpreted as village-level evidence or
as an effect of rainfall, heat, or any individual event.
"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).parents[1]
URL = (
    "https://stats-sdmx-disseminate.pacificdata.org/rest/data/"
    "SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS.TARO.CROP_YIELD"
    "?dimensionAtObservation=AllDimensions"
)
RAW_PATH = ROOT / "data/raw/spc-samoa-taro-yield.csv"
OUTPUT_PATH = ROOT / "public/data/samoa-climate.json"
RETRIEVED = "2026-08-17"


def fetch_csv() -> list[dict[str, str]]:
    request = Request(URL, headers={"Accept": "text/csv", "User-Agent": "Pacific-Dataviz-Challenge-framework/0.2"})
    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(text)
    return list(csv.DictReader(io.StringIO(text)))


def main() -> None:
    rows = fetch_csv()
    expected_columns = {
        "FREQ", "GEO_PICT", "AGRICULTURE_PRODUCTION_ITEM",
        "AGRICULTURE_PRODUCTION_TYPE", "TIME_PERIOD", "OBS_VALUE", "UNIT_MEASURE",
    }
    assert rows and expected_columns.issubset(rows[0]), "Unexpected SPC crop-yield CSV schema"
    assert all(row["FREQ"] == "A" for row in rows), "Expected annual data"
    assert all(row["GEO_PICT"] == "WS" for row in rows), "Expected Samoa data"
    assert all(row["AGRICULTURE_PRODUCTION_ITEM"] == "TARO" for row in rows), "Expected TARO item"
    assert all(row["AGRICULTURE_PRODUCTION_TYPE"] == "CROP_YIELD" for row in rows), "Expected crop yield"
    assert all(row["UNIT_MEASURE"] == "KGHA" for row in rows), "Expected kg/ha unit"

    yield_rows = [[int(row["TIME_PERIOD"]), float(row["OBS_VALUE"])] for row in rows]
    years = [row[0] for row in yield_rows]
    assert years == list(range(1961, 2025)), "Unexpected taro-year coverage or gaps"

    data = json.loads(OUTPUT_PATH.read_text())
    data["taro_yield"] = yield_rows
    data["taro_yield_provenance"] = {
        "source": "Pacific Community (SPC) Pacific Data Hub .Stat — DF_AGRICULTURAL_PRODUCTION",
        "url": URL,
        "retrieved": RETRIEVED,
        "geography": "Samoa (WS); annual national/country context, not village or farm-level evidence",
        "item": "TARO",
        "measure": "CROP_YIELD",
        "unit": "kg/ha",
        "coverage": "1961–2024",
        "warning": "This descriptive series must not be used to infer rainfall or SST caused taro outcomes, or to forecast yield.",
    }
    OUTPUT_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"PASS taro yield: {len(yield_rows)} annual observations, {years[0]}–{years[-1]}")
    print(f"RAW {RAW_PATH.relative_to(ROOT)}")
    print(f"UPDATED {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
