#!/usr/bin/env python3
"""Summarize common eval JSONL logs without assuming one framework schema."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def nested_get(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    current: Any = record
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def first_present(record: dict[str, Any], paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        value = nested_get(record, path)
        if value is not None:
            return value
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize eval JSONL.")
    parser.add_argument("jsonl", help="Path to JSONL log or result file")
    args = parser.parse_args()

    path = Path(args.jsonl).expanduser().resolve()
    total = 0
    invalid = 0
    outcomes: Counter[str] = Counter()
    event_types: Counter[str] = Counter()
    comparable = 0
    exact_passed = 0

    outcome_paths = [
        ("passed",),
        ("correct",),
        ("score",),
        ("result", "passed"),
        ("data", "passed"),
        ("data", "correct"),
        ("data", "score"),
    ]

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue

            event_types[str(record.get("type", "record"))] += 1
            outcome = first_present(record, outcome_paths)
            if outcome is not None:
                outcomes[str(outcome)] += 1
            if "prediction" in record and "ideal" in record:
                comparable += 1
                if str(record["prediction"]).strip().lower() == str(record["ideal"]).strip().lower():
                    exact_passed += 1

    print("# JSONL Eval Summary")
    print(f"file: {path}")
    print(f"records: {total}")
    print(f"invalid_json: {invalid}")
    print("\n## Event Types")
    for key, count in event_types.most_common():
        print(f"- {key}: {count}")
    print("\n## Outcomes")
    if outcomes:
        for key, count in outcomes.most_common():
            print(f"- {key}: {count}")
    elif comparable:
        print(f"- exact_match_passed: {exact_passed}")
        print(f"- exact_match_failed: {comparable - exact_passed}")
        print(f"- exact_match_rate: {exact_passed / comparable:.4f}")
    else:
        print("- No common outcome fields found. Inspect the raw schema before making claims.")


if __name__ == "__main__":
    main()
