from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from .project import find_project_root

REQUIRED = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "MANIFEST.in",
    "skill/SKILL.md",
    "skill/agents/openai.yaml",
    "skill/references/grader-selection.md",
    "skill/references/openai-evals-usage.md",
    "skill/references/sample-design.md",
    "skill/assets/templates/eval-intake.md",
    "skill/assets/templates/samples.jsonl",
    "skill/assets/templates/rubric.md",
    "skill/assets/templates/report-template.md",
    "skill/assets/templates/openai-evals.yaml",
    "skill/assets/templates/checker.py",
    "skill/scripts/create_eval_scaffold.py",
    "skill/scripts/summarize_jsonl.py",
    "skill/scripts/detect_openai_evals.py",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    "src/llm_eval_starter/__init__.py",
    "src/llm_eval_starter/scaffold.py",
    "src/llm_eval_starter/summarize.py",
    "src/llm_eval_starter/detect.py",
    "src/llm_eval_starter/validate.py",
    "src/llm_eval_starter/release.py",
    "src/llm_eval_starter/cli.py",
    "tests/test_project.py",
    "scripts/validate_public_package.py",
    "scripts/build_release.py",
]

SENSITIVE_PATTERNS = [
    r"/Users/[A-Za-z0-9._-]+",
    r"/home/[A-Za-z0-9._-]+",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"OPENAI_API_KEY\s*=\s*[\"'][^\"']+",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"api[_-]?key\s*[:=]\s*[\"'][^\"']{8,}",
    r"password\s*[:=]\s*[\"'][^\"']{8,}",
    r"secret\s*[:=]\s*[\"'][^\"']{8,}",
    r"token\s*[:=]\s*[\"'][^\"']{8,}",
]


def validate_pyproject(root: Path) -> list[str]:
    failures: list[str] = []
    pyproject = root / "pyproject.toml"
    data: dict[str, Any] = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    project = data.get("project", {})
    if not isinstance(project, dict):
        failures.append("pyproject.toml missing [project]")
        return failures

    scripts = project.get("scripts", {})
    if not isinstance(scripts, dict):
        failures.append("pyproject.toml missing [project.scripts]")
    else:
        required_scripts = {
            "llm-eval-starter-validate",
            "llm-eval-starter-summarize",
            "llm-eval-starter-detect",
            "llm-eval-starter-scaffold",
            "llm-eval-starter-build-release",
        }
        missing = required_scripts - set(scripts)
        if missing:
            failures.append(f"pyproject.toml missing scripts: {sorted(missing)}")

    if project.get("name") != "llm-eval-starter-skill":
        failures.append("pyproject.toml project name mismatch")

    return failures


def validate_public_package(root: Path) -> list[str]:
    root = find_project_root(root)
    failures: list[str] = []
    excluded_parts = {"dist", "build", "__pycache__"}

    for rel in REQUIRED:
        if not (root / rel).exists():
            failures.append(f"missing required file: {rel}")

    skill = root / "skill" / "SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""
        for required in ("name:", "version:", "description:"):
            if required not in frontmatter:
                failures.append(f"SKILL.md missing frontmatter field: {required}")

    if (root / "pyproject.toml").exists():
        failures.extend(validate_pyproject(root))

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in excluded_parts or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.suffix not in {".md", ".yaml", ".yml", ".json", ".jsonl", ".py", ".txt", ".toml", ".in"} and path.name not in {"LICENSE", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                failures.append(f"sensitive pattern {pattern!r} in {path.relative_to(root)}")

    return failures
