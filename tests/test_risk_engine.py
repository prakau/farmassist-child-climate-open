from apps.api.schemas import ObservationCreate
from packages.risk_engine import assess_risk


def test_threshold_boundaries(observation: dict[str, object]) -> None:
    observation.update(temperature_c=32, soil_moisture_pct=30, relative_humidity_pct=75)
    result = assess_risk(ObservationCreate.model_validate(observation))
    assert result.heat_stress_risk == "moderate"
    assert result.water_stress_risk == "moderate"
    assert result.humidity_disease_risk == "moderate"


def test_high_temperature(observation: dict[str, object]) -> None:
    observation["temperature_c"] = 41
    assert assess_risk(ObservationCreate.model_validate(observation)).heat_stress_risk == "high"


def test_low_soil_moisture(observation: dict[str, object]) -> None:
    observation["soil_moisture_pct"] = 10
    result = assess_risk(ObservationCreate.model_validate(observation))
    assert result.water_stress_risk == "high"
    assert "agronomic validation" in result.disclaimer
