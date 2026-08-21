# TypeScript AI boundary package

This package is reserved for provider-neutral contracts or a future server-only client for the
private FastAPI service. It must not own provider SDKs, provider credentials, prompts, retrieval,
or model execution.

The provider-owning runtime is `services/ai`. Browsers must never import a client that calls the
AI service or an AI provider directly.

