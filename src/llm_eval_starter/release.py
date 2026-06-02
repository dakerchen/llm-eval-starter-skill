from __future__ import annotations

import shutil
import tomllib
import zipfile
from pathlib import Path
from typing import Iterable


EXCLUDE_NAMES = {
    ".git",
    ".DS_Store",
    "dist",
    "build",
}

EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".zip"}


def _include(path: Path) -> bool:
    if any(part == "__pycache__" for part in path.parts):
        return False
    if any(part in EXCLUDE_NAMES or part.endswith(".egg-info") for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    return True


def _iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and _include(path):
            yield path


def read_version(root: Path) -> str:
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def build_release_zip(root: Path, dist_dir: Path | None = None) -> Path:
    root = root.expanduser().resolve()
    dist_dir = (dist_dir or root / "dist").expanduser().resolve()
    dist_dir.mkdir(parents=True, exist_ok=True)

    version = read_version(root)
    archive = dist_dir / f"llm-eval-starter-skill-v{version}.zip"
    if archive.exists():
        archive.unlink()

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in _iter_files(root):
            zf.write(path, arcname=path.relative_to(root))

    return archive


def clean_dist(root: Path) -> None:
    dist = root / "dist"
    if dist.exists():
        shutil.rmtree(dist)
