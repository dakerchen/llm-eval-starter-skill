#!/usr/bin/env python3
"""Build release artifacts for the public package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_eval_starter.project import find_project_root
from llm_eval_starter.release import build_release_zip, clean_dist


def main() -> int:
    root = find_project_root(PROJECT_ROOT).resolve()
    clean_dist(root)
    try:
        subprocess.run([sys.executable, "-m", "build", "--sdist", "--wheel"], cwd=root, check=True)
    except subprocess.CalledProcessError as exc:
        print("Install the optional release dependency first: python -m pip install -e .[release]")
        raise SystemExit(exc.returncode) from exc
    print(build_release_zip(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
