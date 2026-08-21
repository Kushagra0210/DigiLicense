# DigiLicense AI service

This directory owns the private, stateless AI runtime for DigiLicense. It currently needs no
provider API key: the assistant routes approved public context into a fixed bilingual guidance
catalog after inbound PII screening.

The service must be called by a trusted product server. It is not a browser-facing API and has
no product-database credentials.

## Current safety pipeline

Every assistant request follows this order:

1. Strict request and size validation
2. Unicode NFKC, invisible-character and Devanagari-digit normalization
3. Presidio-backed inbound PII detection
4. Canonical intent routing with confidence thresholds
5. Fixed English or Hindi guidance
6. Outbound PII detection

PII causes the whole question to be blocked. The service does not redact, tokenize, vault, retain,
or forward a modified version. If either DLP pass fails, the request fails closed to static safety
guidance.

The explicit recognizer registry covers Aadhaar, PAN, Indian passport and voter IDs, Indian mobile
numbers, OTPs, driving and learner licence numbers, application and receipt numbers, vehicle
registrations, UPI IDs, IFSC and bank-account patterns, payment cards/secrets, and high-confidence
address or identity phrases. Test fixtures are synthetic and never submitted to external systems.

## Run locally

```bash
cd services/ai
cp .env.example .env
uv sync --dev
uv run uvicorn app.main:app --reload --no-access-log
```

Use the same value from `AI_SERVICE_API_KEY` when calling the private endpoint:

```bash
curl http://127.0.0.1:8000/v1/assistant/messages \
  -H 'Authorization: Bearer replace-with-at-least-32-random-characters' \
  -H 'Content-Type: application/json' \
  --data '{
    "question": "Why is an appointment unavailable?",
    "locale": "en",
    "service": "driving_licence",
    "page": "appointment_waitlist",
    "reasonCode": "NO_MATCHING_SLOT"
  }'
```

Health endpoints are available at `/health/live` and `/health/ready`. Readiness returns `503`
when the service credential is not configured.

## Checks

```bash
uv run ruff check .
uv run pytest
uv run python -m scripts.generate_openapi --check
```

Request and response bodies are intentionally excluded from application logs. Normalized text is
still sensitive and must never be logged. Never add raw questions, answers, authorization headers,
provider prompts, detected spans, identifier values, or evidence text to logs.
