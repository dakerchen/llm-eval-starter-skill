from __future__ import annotations

import re
from pathlib import Path

EVAL_INTAKE = """# Eval Intake

## 1. Evaluation Target

- Target type:
- Target name:
- Target version:
- Owner:

## 2. Decision

- What decision will this eval support?
- What happens if the target fails?
- Is this a release gate, regression check, comparison, or exploratory review?

## 3. Success Standard

- Pass:
- Partial pass:
- Fail:
- Must-block issues:
- Must-review issues:

## 4. Samples

- Source:
- Count:
- Human-approved: yes / no
- Covers normal cases: yes / no
- Covers boundary cases: yes / no
- Covers known failures: yes / no
- Covers high-risk cases: yes / no

## 5. Grader

- Deterministic checks:
- Exact/reference match:
- Rubric scoring:
- LLM-as-judge needed: yes / no
- Human spot-check plan:

## 6. Report

- Audience:
- Decision deadline:
- Sensitive details to remove:
- Output format:

## Gate Decision

- Ready for formal baseline: yes / no
- Current level: formal baseline / draft eval / smoke test / manual review
- Missing information:
"""

RUBRIC = """# Rubric

## Target

Describe the model, prompt, agent, workflow, or AI application being evaluated.

## Decision

State the decision this eval supports.

## Dimensions

### 1. Task Correctness

- Pass: The output completes the requested task and matches the expected outcome.
- Partial: The main outcome is correct, but one secondary requirement is missing or weak.
- Fail: The output is wrong or does not complete the requested task.

### 2. Source Grounding

- Pass: The output only uses facts available in the input or approved context.
- Partial: The output is mostly grounded but contains one minor unsupported claim.
- Fail: The output invents or contradicts material facts.

### 3. Format Stability

- Pass: The output follows the required structure, field names, enum values, and type contract.
- Partial: The output is readable but has minor formatting drift.
- Fail: The output cannot be parsed or used downstream.

### 4. Risk Handling

- Pass: The output handles sensitive, unsafe, or uncertain cases according to policy.
- Partial: The output is cautious but misses one review signal.
- Fail: The output gives unsafe, unsupported, or overconfident guidance.

## Human Review Required When

1. The case affects a high-risk decision.
2. The grader and human reviewer disagree.
3. The output contains unsupported claims.
4. The model refuses or escalates unexpectedly.
"""

REPORT = """# Eval Report

## Judgment

Current result supports: release / limited rollout / more fixes / manual review only.

## Scope

- Target:
- Target version:
- Sample set:
- Sample count:
- Grader:
- Runner:

## Result Summary

| Metric | Value |
|---|---:|
| Total samples |  |
| Passed |  |
| Failed |  |
| Partial |  |
| Pass rate |  |

## Failure Types

| Failure type | Count | Example ids | Likely cause | Action |
|---|---:|---|---|---|
|  |  |  |  |  |

## Decision Notes

1. Confirmed:
2. Likely:
3. Open:

## Next Iteration

1. Fix:
2. Re-run:
3. Add samples:
4. Human review:
"""

SAMPLES = """{"id":"support-login-001","input":[{"role":"system","content":"Classify the support request into one of: login, billing, bug, other. Output only the label."},{"role":"user","content":"I cannot sign in after resetting my password."}],"ideal":"login","tags":["normal","classification"],"risk":"low","notes":"Basic fixed-label classification."}
{"id":"support-billing-001","input":[{"role":"system","content":"Classify the support request into one of: login, billing, bug, other. Output only the label."},{"role":"user","content":"I was charged twice this month."}],"ideal":"billing","tags":["normal","classification"],"risk":"medium","notes":"Billing issue should not be routed to generic support."}
{"id":"support-ambiguous-001","input":[{"role":"system","content":"Classify the support request into one of: login, billing, bug, other. Output only the label."},{"role":"user","content":"The app keeps saying my account is not active, but I paid yesterday."}],"ideal":"billing","tags":["boundary","mixed-intent"],"risk":"medium","notes":"Payment/account activation ambiguity; expected route is billing for first review."}
"""

OPENAI_EVALS = """# Starter OpenAI Evals-style registry config.
# Replace the placeholders with your eval name and folder.

evals:
  __EVAL_ID__:
    id: __EVAL_ID__
    metrics:
      - accuracy
    class: evals.elsuite.basic.match:Match
    args:
      samples_jsonl: __EVAL_FOLDER__/samples.jsonl
"""

CHECKER = """#!/usr/bin/env python3
\"\"\"Example deterministic checker for JSONL classification results.\"\"\"

from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize(value: object) -> str:
    return str(value).strip().lower()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check simple prediction JSONL.")
    parser.add_argument("path", help="JSONL file with id, prediction, and ideal fields")
    args = parser.parse_args()

    path = Path(args.path)
    total = 0
    passed = 0
    failures: list[str] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            record = json.loads(line)
            if normalize(record.get("prediction")) == normalize(record.get("ideal")):
                passed += 1
            else:
                failures.append(str(record.get("id", f"row-{total}")))

    print(json.dumps({
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0,
        "failure_ids": failures,
    }, indent=2))


if __name__ == "__main__":
    main()
"""


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower()).strip("-")
    return slug or "llm-eval"


def create_eval_scaffold(name: str, out_root: Path) -> Path:
    slug = slugify(name)
    eval_id = slug.replace("-", "_") + ".dev.v0"
    out = out_root.expanduser().resolve() / slug

    (out / "data" / slug).mkdir(parents=True, exist_ok=True)
    (out / "reports").mkdir(parents=True, exist_ok=True)
    (out / "registry").mkdir(parents=True, exist_ok=True)
    (out / "scripts").mkdir(parents=True, exist_ok=True)

    (out / "eval-intake.md").write_text(EVAL_INTAKE, encoding="utf-8")
    (out / "data" / slug / "samples.jsonl").write_text(SAMPLES, encoding="utf-8")
    (out / "rubric.md").write_text(RUBRIC, encoding="utf-8")
    (out / "reports" / "report.md").write_text(REPORT, encoding="utf-8")
    (out / "registry" / f"{slug}.yaml").write_text(
        OPENAI_EVALS.replace("__EVAL_ID__", eval_id).replace("__EVAL_FOLDER__", slug),
        encoding="utf-8",
    )
    (out / "scripts" / "checker.py").write_text(CHECKER, encoding="utf-8")

    return out

