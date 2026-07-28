import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from apps.api.schemas import ObservationBase, RiskAssessment

DISCLAIMER = (
    "Reference threshold result only; requires local agronomic validation and human review. "
    "Not an emergency warning or medical, nutrition, or public-health recommendation."
)


@lru_cache
def get_thresholds() -> dict[str, Any]:
    path = Path(__file__).with_name("thresholds.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _level(value: float, moderate: float, high: float, *, reverse: bool = False) -> str:
    if reverse:
        return "high" if value <= high else "moderate" if value <= moderate else "low"
    return "high" if value >= high else "moderate" if value >= moderate else "low"


def assess_risk(observation: ObservationBase) -> RiskAssessment:
    config = get_thresholds()
    heat = _level(observation.temperature_c, **{
        "moderate": config["heat"]["moderate_c"], "high": config["heat"]["high_c"]
    })
    water = _level(
        observation.soil_moisture_pct,
        config["water"]["moderate_pct"],
        config["water"]["high_pct"],
        reverse=True,
    )
    humidity = _level(
        observation.relative_humidity_pct,
        config["humidity"]["moderate_pct"],
        config["humidity"]["high_pct"],
    )
    points = {"low": 0, "moderate": 50, "high": 100}
    score = round(
        points[heat] * config["weights"]["heat"]
        + points[water] * config["weights"]["water"]
        + points[humidity] * config["weights"]["humidity"]
    )
    combined = "high" if score >= 70 else "moderate" if score >= 35 else "low"
    reasons = [
        f"Temperature {observation.temperature_c:.1f}°C gives {heat} heat stress risk.",
        f"Soil moisture {observation.soil_moisture_pct:.1f}% gives {water} water stress risk.",
        f"Humidity {observation.relative_humidity_pct:.1f}% gives {humidity} disease risk.",
    ]
    checks = []
    if heat != "low":
        checks.append("Confirm temperature with a calibrated shaded sensor.")
    if water != "low":
        checks.append("Inspect root-zone moisture and irrigation availability.")
    if humidity != "low":
        checks.append("Inspect leaves for symptoms; consult a qualified agronomist.")
    if not checks:
        checks.append("Continue routine monitoring; conditions can change.")
    return RiskAssessment(
        heat_stress_risk=heat,
        water_stress_risk=water,
        humidity_disease_risk=humidity,
        combined_risk_level=combined,
        risk_score=score,
        reasons=reasons,
        suggested_next_checks=checks,
        disclaimer=DISCLAIMER,
    )
