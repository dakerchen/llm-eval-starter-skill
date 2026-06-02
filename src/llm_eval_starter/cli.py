from __future__ import annotations

import argparse
import json
from pathlib import Path

from .detect import detect_openai_evals
from .release import build_release_zip
from .project import find_project_root
from .scaffold import create_eval_scaffold
from .summarize import summarize_jsonl
from .validate import validate_public_package


def scaffold_cmd() -> None:
    parser = argparse.ArgumentParser(description="Create an eval scaffold.")
    parser.add_argument("name", help="Eval name")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()
    out = create_eval_scaffold(args.name, Path(args.out))
    print(f"Created: {out}")
    print(f"Edit: {out / 'eval-intake.md'}")
    print(f"Edit: {out / 'data' / out.name / 'samples.jsonl'}")
    print(f"Edit: {out / 'rubric.md'}")


def summarize_cmd() -> None:
    parser = argparse.ArgumentParser(description="Summarize a JSONL eval log.")
    parser.add_argument("jsonl", help="Path to JSONL file")
    args = parser.parse_args()
    print(json.dumps(summarize_jsonl(args.jsonl), ensure_ascii=False, indent=2))


def detect_cmd() -> None:
    parser = argparse.ArgumentParser(description="Detect OpenAI Evals locally.")
    parser.add_argument("--cwd", default=".", help="Working directory to inspect")
    args = parser.parse_args()
    print(json.dumps(detect_openai_evals(Path(args.cwd)), ensure_ascii=False, indent=2))


def validate_cmd() -> None:
    parser = argparse.ArgumentParser(description="Validate the public package.")
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()
    failures = validate_public_package(find_project_root(Path(args.root)))
    if failures:
        print("Validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Validation passed.")


def build_release_cmd() -> None:
    parser = argparse.ArgumentParser(description="Build a release zip.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--dist", default=None, help="Output dist directory")
    args = parser.parse_args()
    archive = build_release_zip(find_project_root(Path(args.root)), Path(args.dist) if args.dist else None)
    print(str(archive))
