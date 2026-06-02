#!/usr/bin/env python3
"""Create a small LLM eval starter folder from bundled templates."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower()).strip("-")
    return slug or "llm-eval"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an LLM eval starter scaffold.")
    parser.add_argument("name", help="Evaluation name, for example support-triage")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    templates = skill_dir / "assets" / "templates"
    name = slugify(args.name)
    eval_id = name.replace("-", "_") + ".dev.v0"
    out = Path(args.out).expanduser().resolve() / name

    (out / "data" / name).mkdir(parents=True, exist_ok=True)
    (out / "reports").mkdir(parents=True, exist_ok=True)
    (out / "registry").mkdir(parents=True, exist_ok=True)
    (out / "scripts").mkdir(parents=True, exist_ok=True)

    copy_map = {
        "eval-intake.md": out / "eval-intake.md",
        "samples.jsonl": out / "data" / name / "samples.jsonl",
        "rubric.md": out / "rubric.md",
        "report-template.md": out / "reports" / "report.md",
        "checker.py": out / "scripts" / "checker.py",
    }

    for src_name, dest in copy_map.items():
        shutil.copyfile(templates / src_name, dest)

    yaml_text = (templates / "openai-evals.yaml").read_text(encoding="utf-8")
    yaml_text = yaml_text.replace("__EVAL_ID__", eval_id).replace("__EVAL_FOLDER__", name)
    (out / "registry" / f"{name}.yaml").write_text(yaml_text, encoding="utf-8")

    print(f"Created: {out}")
    print("Edit these first:")
    print(f"1. {out / 'eval-intake.md'}")
    print(f"2. {out / 'data' / name / 'samples.jsonl'}")
    print(f"3. {out / 'rubric.md'}")
    print("Label the set as smoke/draft until samples and rubric are human-approved.")


if __name__ == "__main__":
    main()
