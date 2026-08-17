"""Fetch reproducible monthly precipitation data from NASA/POWER for a Samoa grid point.

This is a gridded MERRA-2-derived product, not Samoa-wide observations or station data.
It is kept separate from the official SPC annual rainfall-anomaly series.
"""
import calendar
import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/nasa-power-upolu-monthly-precipitation-1981-2025.json"
PROCESSED = ROOT / "data/processed/nasa-power-upolu-monthly-precipitation-1981-2025.csv"
LATITUDE = -13.83
LONGITUDE = -171.75
PARAMETERS = {
    "parameters": "PRECTOTCORR",
    "community": "AG",
    "longitude": LONGITUDE,
    "latitude": LATITUDE,
    "start": 1981,
    "end": 2025,
    "format": "JSON",
}
URL = "https://power.larc.nasa.gov/api/temporal/monthly/point?" + urlencode(PARAMETERS)


def main() -> None:
    with urlopen(URL, timeout=60) as response:
        payload = json.load(response)
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(payload, indent=2) + "\n")

    values = payload["properties"]["parameter"]["PRECTOTCORR"]
    rows = []
    for key, value in sorted(values.items()):
        if len(key) != 6 or key.endswith("13") or value == payload["header"]["fill_value"]:
            continue
        year, month = int(key[:4]), int(key[4:])
        rows.append({
            "year": year,
            "month": month,
            "mean_daily_precipitation_mm": value,
            "derived_monthly_total_mm": round(value * calendar.monthrange(year, month)[1], 3),
        })
    if len(rows) != 45 * 12:
        raise RuntimeError(f"Expected 540 monthly rows; got {len(rows)}")

    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({
        "url": URL,
        "source": payload["header"]["sources"],
        "coverage": [rows[0]["year"], rows[-1]["year"]],
        "rows": len(rows),
        "coordinate": {"latitude": LATITUDE, "longitude": LONGITUDE},
        "raw": str(RAW.relative_to(ROOT)),
        "processed": str(PROCESSED.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
