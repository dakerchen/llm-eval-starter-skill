from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from typing import Any


def detect_openai_evals(cwd: Path | None = None) -> dict[str, Any]:
    cwd = (cwd or Path.cwd()).expanduser().resolve()
    commands = {name: shutil.which(name) for name in ("oaieval", "oaievalset")}
    spec = importlib.util.find_spec("evals")
    package = spec.origin if spec and spec.origin else None
    markers = {
        str(cwd / "evals" / "registry"): (cwd / "evals" / "registry").exists(),
        str(cwd / "evals" / "elsuite"): (cwd / "evals" / "elsuite").exists(),
        str(cwd / "pyproject.toml"): (cwd / "pyproject.toml").exists(),
    }

    if any(commands.values()) or package:
        interpretation = "Execution layer found. Start with a smoke eval before creating a baseline."
    else:
        interpretation = "No execution layer found in this shell. Install OpenAI Evals or use another eval runner."

    return {
        "commands": commands,
        "package": package,
        "markers": markers,
        "interpretation": interpretation,
    }

