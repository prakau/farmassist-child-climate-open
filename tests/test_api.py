from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    assert client.get("/health").json()["status"] == "ok"


def test_submit_and_duplicate(client: TestClient, observation: dict[str, object]) -> None:
    assert client.post("/v1/observations", json=observation).status_code == 201
    assert client.post("/v1/observations", json=observation).status_code == 409
    assert len(client.get("/v1/observations").json()) == 1
    assert client.get("/v1/sites/DEMO-001/summary").status_code == 200


def test_missing_site(client: TestClient) -> None:
    assert client.get("/v1/sites/DEMO-999/summary").status_code == 404


def test_public_indicators_are_aggregate(
    client: TestClient, observation: dict[str, object]
) -> None:
    client.post("/v1/observations", json=observation)
    payload = client.get("/v1/public/indicators").json()
    assert payload["valid_environmental_observations"] == 1
    assert payload["active_non_identifying_sites"] == 1
    assert "notes" not in payload
    assert "crop_type" not in payload


def test_risk_and_config(client: TestClient, observation: dict[str, object]) -> None:
    assert client.post("/v1/risk/assess", json=observation).status_code == 200
    assert client.get("/v1/config/risk-thresholds").json()["heat"]["high_c"] == 38
