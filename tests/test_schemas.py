import pytest
from pydantic import ValidationError

from apps.api.schemas import ObservationCreate


def test_valid_schema(observation: dict[str, object]) -> None:
    assert ObservationCreate.model_validate(observation).site_code == "DEMO-001"


@pytest.mark.parametrize(
    ("field", "value"),
    [("temperature_c", 70), ("relative_humidity_pct", 101), ("soil_moisture_pct", -1)],
)
def test_invalid_units(observation: dict[str, object], field: str, value: float) -> None:
    observation[field] = value
    with pytest.raises(ValidationError):
        ObservationCreate.model_validate(observation)


def test_missing_required_field(observation: dict[str, object]) -> None:
    del observation["site_code"]
    with pytest.raises(ValidationError):
        ObservationCreate.model_validate(observation)


def test_rejects_personal_note(observation: dict[str, object]) -> None:
    observation["notes"] = "Phone details"
    with pytest.raises(ValidationError):
        ObservationCreate.model_validate(observation)
