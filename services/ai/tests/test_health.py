from fastapi.testclient import TestClient

from app.config import Environment, Settings
from app.main import create_app


def test_liveness(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_readiness_when_configured(client: TestClient) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_and_assistant_fail_closed_without_service_key(
    valid_payload: dict[str, str],
) -> None:
    settings = Settings(_env_file=None, environment=Environment.TEST, service_api_key=None)

    with TestClient(create_app(settings)) as client:
        readiness = client.get("/health/ready")
        assistant = client.post("/v1/assistant/messages", json=valid_payload)

    assert readiness.status_code == 503
    assert readiness.json() == {"status": "not_ready"}
    assert assistant.status_code == 503

