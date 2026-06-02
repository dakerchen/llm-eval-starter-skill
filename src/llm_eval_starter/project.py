from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | str | None = None) -> Path:
    path = Path(start or Path.cwd()).expanduser().resolve()
    for candidate in [path, *path.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "skill" / "SKILL.md").exists():
            return candidate
    return path

