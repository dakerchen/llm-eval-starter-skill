#!/usr/bin/env python3
"""Validate that the public package is structurally complete and de-sensitized."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_eval_starter.validate import validate_public_package


def main() -> int:
    failures = validate_public_package(PROJECT_ROOT)
    if failures:
        print("Public package validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Public package validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
