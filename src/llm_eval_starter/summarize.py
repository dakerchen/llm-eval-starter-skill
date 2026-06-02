from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def _nested_get(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    current: Any = record
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _first_present(record: dict[str, Any], paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        value = _nested_get(record, path)
        if value is not None:
            return value
    return None


def summarize_jsonl(path: Path | str) -> dict[str, Any]:
    path = Path(path).expanduser().resolve()
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
            outcome = _first_present(record, outcome_paths)
            if outcome is not None:
                outcomes[str(outcome)] += 1
            if "prediction" in record and "ideal" in record:
                comparable += 1
                if str(record["prediction"]).strip().lower() == str(record["ideal"]).strip().lower():
                    exact_passed += 1

    result: dict[str, Any] = {
        "file": str(path),
        "records": total,
        "invalid_json": invalid,
        "event_types": dict(event_types),
        "outcomes": dict(outcomes),
    }
    if outcomes:
        result["exact_match_passed"] = None
        result["exact_match_failed"] = None
        result["exact_match_rate"] = None
    elif comparable:
        result["exact_match_passed"] = exact_passed
        result["exact_match_failed"] = comparable - exact_passed
        result["exact_match_rate"] = exact_passed / comparable
    else:
        result["exact_match_passed"] = None
        result["exact_match_failed"] = None
        result["exact_match_rate"] = None
        result["note"] = "No common outcome fields found. Inspect the raw schema before making claims."

    return result

