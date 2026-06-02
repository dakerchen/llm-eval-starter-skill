#!/usr/bin/env python3
"""Detect OpenAI Evals command/package without assuming private paths."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


def main() -> None:
    print("# OpenAI Evals Detection")

    print("\n## Commands")
    for command in ("oaieval", "oaievalset"):
        print(f"{command}: {shutil.which(command) or 'not found'}")

    print("\n## Python Package")
    spec = importlib.util.find_spec("evals")
    if spec and spec.origin:
        print(f"evals: {spec.origin}")
    else:
        print("evals: not found in current Python")

    print("\n## Common Local Repository Markers")
    cwd = Path.cwd()
    markers = [
        cwd / "evals" / "registry",
        cwd / "evals" / "elsuite",
        cwd / "pyproject.toml",
    ]
    for marker in markers:
        print(f"{marker}: {'found' if marker.exists() else 'not found'}")

    print("\n## Interpretation")
    if shutil.which("oaieval") or (spec and spec.origin):
        print("Execution layer found. Start with a smoke eval before creating a baseline.")
    else:
        print("No execution layer found in this shell. Install OpenAI Evals or use another eval runner.")


if __name__ == "__main__":
    main()
