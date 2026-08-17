"""Minimal reproducible quality checks for the initial Samoa climate framework."""
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
print("PASS: framework source data are structurally valid")
