"""Generate or verify the committed AI service OpenAPI contract."""

import argparse
import json
from pathlib import Path

from app.main import app

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "contracts" / "ai.openapi.json"


def rendered_contract() -> str:
    return json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when the committed contract is stale.",
    )
    args = parser.parse_args()
    rendered = rendered_contract()

    if args.check:
        if not CONTRACT_PATH.exists() or CONTRACT_PATH.read_text() != rendered:
            print(f"OpenAPI contract is stale: {CONTRACT_PATH}")
            return 1
        print(f"OpenAPI contract is current: {CONTRACT_PATH}")
        return 0

    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(rendered)
    print(f"Wrote {CONTRACT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

