#!/usr/bin/env python3
"""Example deterministic checker for JSONL classification results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize(value: object) -> str:
    return str(value).strip().lower()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check simple prediction JSONL.")
    parser.add_argument("path", help="JSONL file with id, prediction, and ideal fields")
    args = parser.parse_args()

    path = Path(args.path)
    total = 0
    passed = 0
    failures: list[str] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            record = json.loads(line)
            if normalize(record.get("prediction")) == normalize(record.get("ideal")):
                passed += 1
            else:
                failures.append(str(record.get("id", f"row-{total}")))

    print(json.dumps({
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0,
        "failure_ids": failures,
    }, indent=2))


if __name__ == "__main__":
    main()
