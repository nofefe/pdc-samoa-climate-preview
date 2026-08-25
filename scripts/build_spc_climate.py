"""Capture and deterministically rebuild SPC Samoa climate chart data.

Default mode rebuilds ``public/data/samoa-climate.json`` only from committed raw
SDMX XML captures. Pass ``--refresh`` deliberately to replace those captures
from the public SPC/Pacific Data Hub API and update their checksum manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_PATH = ROOT / "public" / "data" / "samoa-climate.json"
MANIFEST_PATH = RAW_DIR / "spc-climate-captures.json"
BASE_URL = "https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0"
SOURCES = {
    "rainfall": {
        "indicator": "RAIN_ANOM",
        "url": f"{BASE_URL}/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions",
        "path": RAW_DIR / "spc-samoa-rainfall-anomaly.xml",
        "unit": "MM",
        "baseline": "1991–2020",
        "coverage": range(1979, 2026),
    },
    "sst": {
        "indicator": "SST_ANOM",
        "url": f"{BASE_URL}/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions",
        "path": RAW_DIR / "spc-samoa-eez-sst-anomaly.xml",
        "unit": "CELSIUS",
        "baseline": "1971–2000",
        "coverage": range(1979, 2026),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh() -> dict[str, dict[str, str]]:
    """Download the exact public SDMX responses and record acquisition metadata."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    retrieved_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    records: dict[str, dict[str, str]] = {}
    for name, source in SOURCES.items():
        request = Request(source["url"], headers={"User-Agent": "pdc-samoa-climate-preview/1.0 reproducibility capture"})
        with urlopen(request, timeout=60) as response:
            body = response.read()
            content_type = response.headers.get("content-type", "")
        if not body.startswith(b"<?xml"):
            raise RuntimeError(f"{name}: expected SDMX XML response")
        source["path"].write_bytes(body)
        records[name] = {
            "url": source["url"],
            "path": str(source["path"].relative_to(ROOT)),
            "sha256": sha256(source["path"]),
            "bytes": str(len(body)),
            "content_type": content_type,
            "retrieved_at_utc": retrieved_at,
        }
    MANIFEST_PATH.write_text(json.dumps({"captures": records}, indent=2) + "\n")
    return records


def parse_series(name: str) -> list[list[float | int]]:
    source = SOURCES[name]
    path = source["path"]
    if not path.exists():
        raise FileNotFoundError(f"Missing {path.relative_to(ROOT)}; run with --refresh first.")
    rows: list[list[float | int]] = []
    for observation in ET.parse(path).getroot().iter():
        if not observation.tag.endswith("Obs"):
            continue
        values = {node.attrib.get("id"): node.attrib.get("value") for node in observation.iter() if node.tag.endswith("Value")}
        observed = next((node.attrib["value"] for node in observation.iter() if node.tag.endswith("ObsValue")), None)
        year = values.get("TIME_PERIOD")
        error = values.get("ERROR_VAL")
        if observed is None or year is None or error is None:
            continue
        if values.get("FREQ") != "A" or values.get("GEO_PICT") != "WS" or values.get("CLIMATE_CHANGE_INDICATORS") != source["indicator"]:
            continue
        if values.get("UNIT_MEASURE") != source["unit"] or values.get("ERROR_TYPE") != "SE":
            raise AssertionError(f"{name}: unexpected unit or error metadata")
        if int(year) not in source["coverage"]:
            continue
        rows.append([int(year), float(observed), float(error)])
    rows.sort(key=lambda row: row[0])
    expected_years = list(source["coverage"])
    if [row[0] for row in rows] != expected_years:
        raise AssertionError(f"{name}: unexpected year coverage")
    return rows


def build() -> None:
    rainfall = parse_series("rainfall")
    sst = parse_series("sst")
    captures = json.loads(MANIFEST_PATH.read_text())["captures"]
    for name, source in SOURCES.items():
        if captures[name]["sha256"] != sha256(source["path"]):
            raise AssertionError(f"{name}: raw capture checksum does not match manifest")
    output = {
        "provenance": {
            "source": "Pacific Community (SPC) Pacific Data Hub .Stat — DF_CLIMATE_CHANGE",
            "raw_capture_manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "geography": "Samoa (WS); rainfall is Samoa-wide with aggregation method not stated in inspected metadata, while SST is an EEZ aggregate",
            "warning": "Scope-limited data only. Not village, catchment, coastal or operational forecast data.",
        },
        "rainfall": rainfall,
        "sst": sst,
    }
    existing = json.loads(OUTPUT_PATH.read_text())
    output["taro_yield"] = existing["taro_yield"]
    output["taro_yield_provenance"] = existing["taro_yield_provenance"]
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")
    print(f"PASS rainfall: {len(rainfall)} annual observations")
    print(f"PASS sst: {len(sst)} annual observations")
    print(f"UPDATED {OUTPUT_PATH.relative_to(ROOT)} from committed SPC captures")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="download and checksum fresh raw SPC SDMX responses")
    args = parser.parse_args()
    if args.refresh:
        refresh()
    build()
