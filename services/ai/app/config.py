"""Environment-backed configuration for the AI service."""

from enum import StrEnum

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Validated process configuration.

    The service can boot without a credential in development so liveness remains observable,
    but it will not report ready or serve assistant requests in that state. Production fails
    during configuration loading when the credential is absent.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "DigiLicense AI"
    environment: Environment = Environment.DEVELOPMENT
    service_api_key: SecretStr | None = Field(default=None, min_length=32)
    log_level: str = "INFO"
    max_request_body_bytes: int = Field(default=2_048, ge=1_024, le=16_384)
    max_question_chars: int = Field(default=500, ge=1, le=500)
    intent_confidence_threshold: float = Field(default=0.75, ge=0.5, le=1.0)
    dlp_score_threshold: float = Field(default=0.45, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def require_production_credential(self) -> "Settings":
        if self.environment is Environment.PRODUCTION and self.service_api_key is None:
            raise ValueError("AI_SERVICE_API_KEY is required in production")
        return self


def get_settings() -> Settings:
    """Load settings once during application construction."""

    return Settings()
