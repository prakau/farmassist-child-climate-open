import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite://"

from apps.api.database import Base, engine  # noqa: E402
from apps.api.main import app  # noqa: E402


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def observation() -> dict[str, object]:
    return {
        "observation_id": "00000000-0000-4000-8000-000000000001",
        "timestamp_utc": "2026-01-01T06:00:00Z",
        "site_code": "DEMO-001",
        "temperature_c": 30,
        "relative_humidity_pct": 60,
        "soil_moisture_pct": 40,
        "crop_stage": "vegetative",
        "crop_type": "tomato",
        "observation_source": "synthetic",
        "consent_status": "not_required_synthetic",
        "synchronization_status": "synchronized",
        "approximate_region": "Demo region",
        "notes": "Synthetic demonstration record",
    }
