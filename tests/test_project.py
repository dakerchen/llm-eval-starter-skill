from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_eval_starter.detect import detect_openai_evals
from llm_eval_starter.release import build_release_zip
from llm_eval_starter.scaffold import create_eval_scaffold
from llm_eval_starter.summarize import summarize_jsonl
from llm_eval_starter.validate import validate_public_package


class ProjectTests(unittest.TestCase):
    def test_validate_public_package(self) -> None:
        failures = validate_public_package(ROOT)
        self.assertEqual(failures, [], msg="\n".join(failures))

    def test_create_eval_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = create_eval_scaffold("support-triage", Path(tmp))
            expected = [
                out / "eval-intake.md",
                out / "data" / "support-triage" / "samples.jsonl",
                out / "rubric.md",
                out / "reports" / "report.md",
                out / "registry" / "support-triage.yaml",
                out / "scripts" / "checker.py",
            ]
            for path in expected:
                self.assertTrue(path.exists(), path)

    def test_summarize_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"id": "a", "prediction": "login", "ideal": "login"}),
                        json.dumps({"id": "b", "prediction": "other", "ideal": "billing"}),
                    ]
                ),
                encoding="utf-8",
            )
            summary = summarize_jsonl(path)
            self.assertEqual(summary["records"], 2)
            self.assertEqual(summary["exact_match_passed"], 1)
            self.assertEqual(summary["exact_match_failed"], 1)

    def test_detect_openai_evals(self) -> None:
        data = detect_openai_evals(Path.cwd())
        self.assertIn("commands", data)
        self.assertIn("package", data)
        self.assertIn("interpretation", data)

    def test_build_release_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive = build_release_zip(ROOT, Path(tmp))
            self.assertTrue(archive.exists())
            self.assertTrue(archive.name.endswith(".zip"))


if __name__ == "__main__":
    unittest.main()

