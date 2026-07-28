#!/usr/bin/env python3
import csv
import json
import math
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

SITES = {
    "DEMO-001": "normal",
    "DEMO-002": "heat_stress",
    "DEMO-003": "low_soil_moisture",
}
FIELDS = [
    "observation_id",
    "timestamp_utc",
    "site_code",
    "temperature_c",
    "relative_humidity_pct",
    "soil_moisture_pct",
    "crop_stage",
    "crop_type",
    "observation_source",
    "consent_status",
    "synchronization_status",
    "approximate_region",
    "notes",
]


def generate(output_dir: Path, *, seed: int = 2026) -> list[dict[str, object]]:
    rng = random.Random(seed)
    start = datetime(2026, 4, 1, tzinfo=UTC)
    rows: list[dict[str, object]] = []
    for site, scenario in SITES.items():
        for step in range(30 * 4):
            timestamp = start + timedelta(hours=6 * step)
            daily = math.sin((timestamp.hour - 6) / 24 * 2 * math.pi)
            temperature = 28 + 6 * daily + rng.uniform(-1, 1)
            moisture = 46 - step * 0.05 + rng.uniform(-2, 2)
            if scenario == "heat_stress" and 25 <= step < 60:
                temperature += 10
            if scenario == "low_soil_moisture":
                moisture -= min(30, step * 0.35)
            row: dict[str, object] = {
                "observation_id": str(uuid5(NAMESPACE_URL, f"{site}-{timestamp.isoformat()}")),
                "timestamp_utc": timestamp.isoformat().replace("+00:00", "Z"),
                "site_code": site,
                "temperature_c": round(temperature, 1),
                "relative_humidity_pct": round(
                    max(25, min(95, 72 - 18 * daily + rng.uniform(-3, 3))), 1
                ),
                "soil_moisture_pct": round(max(8, min(75, moisture)), 1),
                "crop_stage": "vegetative" if step < 60 else "flowering",
                "crop_type": "demonstration crop",
                "observation_source": "synthetic",
                "consent_status": "not_required_synthetic",
                "synchronization_status": "synchronized",
                "approximate_region": "Synthetic demonstration region",
                "notes": f"SYNTHETIC DATA — {scenario} scenario",
            }
            rows.append(row)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "observations.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )
    with (output_dir / "observations.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    generate(Path(__file__).parents[1] / "data" / "synthetic")
