import logging

import pytest
from fastapi.testclient import TestClient


def test_valid_request_returns_canonical_fallback(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    response = client.post(
        "/v1/assistant/messages",
        headers=auth_headers,
        json=valid_payload,
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": (
            "No matching synthetic appointment is currently available for the selected "
            "preferences. You can adjust the preferences or join the DigiLicense waitlist."
        ),
        "sourceIds": [],
        "uncertain": False,
        "escalation": None,
        "fallbackUsed": True,
        "blockedReason": None,
    }


def test_extra_fields_are_rejected(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    payload = {**valid_payload, "mobileNumber": "synthetic-forbidden-field"}

    response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 422
    assert response.json()["errors"][0]["type"] == "extra_forbidden"
    assert "synthetic-forbidden-field" not in response.text


def test_invalid_enum_is_rejected_without_echoing_input(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    payload = {**valid_payload, "service": "not-a-real-service"}

    response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 422
    assert "not-a-real-service" not in response.text


def test_oversized_question_is_rejected(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    payload = {**valid_payload, "question": "q" * 501}

    response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 422
    assert "q" * 501 not in response.text


def test_oversized_body_is_rejected_before_validation(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    payload = {**valid_payload, "unexpected": "x" * 3_000}

    response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 413
    assert response.json() == {"detail": "Request body too large"}


def test_missing_service_authentication_is_rejected(
    client: TestClient,
    valid_payload: dict[str, str],
) -> None:
    response = client.post("/v1/assistant/messages", json=valid_payload)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_invalid_service_authentication_is_rejected(
    client: TestClient,
    valid_payload: dict[str, str],
) -> None:
    response = client.post(
        "/v1/assistant/messages",
        headers={"Authorization": "Bearer definitely-not-the-service-key"},
        json=valid_payload,
    )

    assert response.status_code == 401


def test_request_response_and_credentials_are_not_logged(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    request_marker = "PRIVATE_QUESTION_MARKER"
    response_marker = "No matching synthetic appointment"
    credential_marker = auth_headers["Authorization"].split(" ", maxsplit=1)[1]
    payload = {**valid_payload, "question": request_marker}

    with caplog.at_level(logging.INFO, logger="digilicense.ai.requests"):
        response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 200
    log_text = caplog.text
    assert request_marker not in log_text
    assert response_marker not in log_text
    assert credential_marker not in log_text
    assert "route=assistant_messages" in log_text


def test_unknown_raw_path_is_replaced_with_safe_log_label(
    client: TestClient,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path_marker = "6000000000"

    with caplog.at_level(logging.INFO, logger="digilicense.ai.requests"):
        response = client.get(f"/unknown/{path_marker}")

    application_logs = "\n".join(
        record.getMessage()
        for record in caplog.records
        if record.name == "digilicense.ai.requests"
    )
    assert response.status_code == 404
    assert path_marker not in application_logs
    assert "route=unmatched" in application_logs


def test_raw_uvicorn_access_logger_is_disabled(test_app: object) -> None:
    _ = test_app
    assert logging.getLogger("uvicorn.access").disabled is True


def test_hindi_request_returns_deterministic_hindi_guidance(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
) -> None:
    payload = {
        **valid_payload,
        "question": "वेटलिस्ट कैसे काम करती है?",
        "locale": "hi",
        "reasonCode": "WAITLIST_ACTIVE",
    }

    response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 200
    assert "सिंथेटिक वेटलिस्ट" in response.json()["answer"]
    assert response.json()["blockedReason"] is None


def test_pii_request_is_absent_from_response_and_all_logs(
    client: TestClient,
    auth_headers: dict[str, str],
    valid_payload: dict[str, str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    pii_marker = "60000 00000"
    payload = {**valid_payload, "question": f"My mobile is {pii_marker}"}

    with caplog.at_level(logging.INFO):
        response = client.post("/v1/assistant/messages", headers=auth_headers, json=payload)

    assert response.status_code == 200
    assert response.json()["blockedReason"] == "PII_DETECTED"
    assert pii_marker not in response.text
    assert pii_marker not in caplog.text
