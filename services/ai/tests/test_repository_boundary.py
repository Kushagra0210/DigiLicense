import json
from pathlib import Path


def test_typescript_boundary_does_not_own_provider_sdks() -> None:
    package_path = Path(__file__).resolve().parents[3] / "packages" / "ai" / "package.json"
    package = json.loads(package_path.read_text())
    dependencies = {
        **package.get("dependencies", {}),
        **package.get("devDependencies", {}),
    }

    forbidden_packages = {"openai", "@anthropic-ai/sdk", "@google/generative-ai"}
    assert forbidden_packages.isdisjoint(dependencies)

