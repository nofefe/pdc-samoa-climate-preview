"""Minimal reproducible quality checks for the Samoa climate story data."""
import json
from pathlib import Path

path = Path(__file__).parents[1] / "public/data/samoa-climate.json"
data = json.loads(path.read_text())
for name, expected_start, expected_end in (("rainfall", 1979, 2025), ("sst", 1979, 2025)):
    rows = data[name]
    years = [row[0] for row in rows]
    assert years == list(range(expected_start, expected_end + 1)), f"{name}: non-contiguous years"
    assert all(isinstance(row[1], (int, float)) for row in rows), f"{name}: non-numeric value"
    assert all(row[2] >= 0 for row in rows), f"{name}: negative standard error"
    print(f"PASS {name}: {len(rows)} annual observations, {years[0]}–{years[-1]}")

taro = data["taro_yield"]
taro_years = [row[0] for row in taro]
assert taro_years == list(range(1961, 2025)), "taro_yield: unexpected coverage or gaps"
assert all(isinstance(row[1], (int, float)) and row[1] >= 0 for row in taro), "taro_yield: invalid yield value"
assert data["taro_yield_provenance"]["item"] == "TARO", "taro_yield: wrong item"
assert data["taro_yield_provenance"]["unit"] == "kg/ha", "taro_yield: wrong unit"
print(f"PASS taro_yield: {len(taro)} annual observations, {taro_years[0]}–{taro_years[-1]}")
print("PASS: story source data are structurally valid")
