import csv
import json
from pathlib import Path

from scripts.generate_synthetic_data import generate


def test_generator_writes_deterministic_csv_and_json(tmp_path: Path) -> None:
    rows = generate(tmp_path)
    assert len(rows) == 3 * 30 * 4
    assert {row["site_code"] for row in rows} == {"DEMO-001", "DEMO-002", "DEMO-003"}
    assert all(row["observation_source"] == "synthetic" for row in rows)
    assert len(json.loads((tmp_path / "observations.json").read_text())) == len(rows)
    with (tmp_path / "observations.csv").open() as handle:
        assert len(list(csv.DictReader(handle))) == len(rows)
    assert max(row["temperature_c"] for row in rows if row["site_code"] == "DEMO-002") >= 38
    assert min(row["soil_moisture_pct"] for row in rows if row["site_code"] == "DEMO-003") <= 18
