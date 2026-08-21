from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.config import Environment, Settings
from app.main import create_app

TEST_SERVICE_KEY = "synthetic-test-service-key-that-is-not-secret"


@pytest.fixture
def settings() -> Settings:
    return Settings(
        _env_file=None,
        environment=Environment.TEST,
        service_api_key=SecretStr(TEST_SERVICE_KEY),
        max_request_body_bytes=2_048,
        max_question_chars=500,
    )


@pytest.fixture
def test_app(settings: Settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture
def client(test_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {TEST_SERVICE_KEY}"}


@pytest.fixture
def valid_payload() -> dict[str, str]:
    return {
        "question": "Why is an appointment unavailable?",
        "locale": "en",
        "service": "driving_licence",
        "page": "appointment_waitlist",
        "reasonCode": "NO_MATCHING_SLOT",
    }

