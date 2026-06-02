---
name: llm-eval-starter
version: "1.0.0"
description: Turn ad-hoc AI quality checks into a small, decision-ready eval package. Use when the user wants to decide whether a model, prompt, agent, RAG flow, workflow, or AI application is ready to ship; create test samples, rubrics, deterministic checks, baseline reports, or an OpenAI Evals-compatible starter scaffold; or compare versions with a repeatable evaluation loop.
---

# LLM Eval Starter

Use this skill to turn informal AI quality feedback into a small, repeatable evaluation loop.

The goal is not to rank models in general. The goal is to decide whether a specific AI behavior is good enough for a specific product, workflow, or business use case.

## When To Use

Use when the user wants to:

1. Evaluate a model, prompt, agent, RAG flow, workflow, or AI application.
2. Build a starter eval set, rubric, grader, or quality gate.
3. Compare two versions of a prompt, model, tool chain, or workflow.
4. Turn manual QA examples into a reusable regression set.
5. Create an OpenAI Evals-compatible scaffold without copying OpenAI Evals itself.

Do not use when:

1. The use case is still undefined and no success standard exists.
2. The user only has a one-off demo and does not need regression.
3. The user wants a generic model benchmark rather than task-specific evaluation.
4. The user has no examples, no expected behavior, and no human owner for quality decisions.

## Core Positioning

The evaluation package has four layers:

1. **Human judgment** defines the task, success standard, examples, and risk boundaries.
2. **Skill workflow** designs the eval scope, grader strategy, sample structure, and report.
3. **Execution layer** runs the eval with OpenAI Evals, another runner, or a local script.
4. **Templates and scripts** reduce setup cost for samples, rubrics, reports, and log summaries.

Do not copy third-party eval framework source code into the skill. Treat frameworks such as OpenAI Evals as external execution layers.

## First Response Gate

Before creating a formal eval, classify the user's situation:

| Situation | Output |
|---|---|
| Clear task, success standard, examples, and report audience | Eval plan + scaffold |
| Clear task and examples, but weak success standard | Draft rubric + questions |
| Only a few ad hoc examples | Smoke test + manual review table |
| Only a product idea | Eval intake checklist |
| Execution framework not installed | Setup check before formal run |

Never call a few unreviewed examples a "quality baseline." Label them as smoke tests or draft eval samples.

## Required Inputs

Collect or infer these before generating a formal eval:

1. **Evaluation target**: model, prompt, agent, RAG flow, workflow, or complete AI application.
2. **Version**: current prompt/model/config/version being tested.
3. **Success standard**: what counts as pass, fail, partial pass, and must-block.
4. **Sample source**: real cases, golden set, historical failures, synthetic examples, or temporary smoke examples.
5. **Report audience**: product, engineering, operations, compliance, customers, or public readers.
6. **Decision use**: release gate, regression check, prompt comparison, risk review, or exploratory diagnosis.

If any input is missing and would change the eval design, ask only the missing high-impact questions.

## Evaluation Flow

1. **Decide whether evaluation is warranted**
   - Use evals when the behavior repeats, quality affects decisions, and versions will change.
   - Use manual review when the need is exploratory or examples are too few.

2. **Define observable dimensions**
   - Good dimensions are visible in outputs: factuality, completeness, format validity, tool-use correctness, citation support, safety, refusal behavior, or actionability.
   - Avoid vague dimensions such as "high quality" or "sounds good."

3. **Split samples**
   - Smoke: 1-3 examples to verify the runner and output format.
   - Core set: 5-20 examples covering expected behavior and known risks.
   - Failure set: previous misses that must not regress.
   - Full regression: larger set used only after the small sets are stable.

4. **Choose grader strategy**
   - Prefer deterministic checks first.
   - Use exact match for fixed labels.
   - Use reference answers for extraction, QA, and summaries.
   - Use rubric scoring for judgment-heavy outputs.
   - Use LLM-as-judge only when semantic judgment cannot be reduced to rules.

5. **Run baseline before changing anything**
   - Save score, failure examples, grader version, sample version, and target version.
   - Do not modify prompt, rubric, and samples in the same iteration.

6. **Change one variable per round**
   - Valid variables: prompt, model, retrieval settings, tool instructions, rubric, sample set, or grader.
   - Re-run the same sample set before claiming improvement.

7. **Report for decisions**
   - State whether the result is enough for the next decision.
   - Show failure types, not just average scores.
   - Separate confirmed findings, likely causes, and open questions.

## Grader Selection

Read `references/grader-selection.md` when the grader choice matters.

Default order:

1. Rule checks.
2. Exact match.
3. Reference answer match.
4. Rubric scoring.
5. LLM-as-judge.

Use strong gates for format, safety, compliance, citations, factual boundaries, fixed labels, and required fields.

Use weak gates for tone, depth, usefulness, and other subjective qualities that still need human review.

## Starter Assets

Use the bundled assets when creating a project:

| Need | File |
|---|---|
| Intake checklist | `assets/templates/eval-intake.md` |
| Sample JSONL | `assets/templates/samples.jsonl` |
| Rubric | `assets/templates/rubric.md` |
| Report | `assets/templates/report-template.md` |
| OpenAI Evals YAML starter | `assets/templates/openai-evals.yaml` |
| Example deterministic checker | `assets/templates/checker.py` |

Use scripts when deterministic setup or log parsing is needed:

| Need | Script |
|---|---|
| Create a starter eval folder | `scripts/create_eval_scaffold.py` |
| Summarize an eval JSONL log | `scripts/summarize_jsonl.py` |
| Detect local OpenAI Evals command/package | `scripts/detect_openai_evals.py` |

## OpenAI Evals Boundary

OpenAI Evals is an execution layer. This skill can generate starter YAML, samples, rubrics, and reports, but it does not vendor OpenAI Evals.

When using OpenAI Evals:

1. Check whether `oaieval` or the `evals` Python package exists.
2. If not found, ask the user to install or point to their runner.
3. Start with a small smoke eval.
4. Inspect logs before scaling to a larger set.
5. Record framework version and runner command in the report.

Read `references/openai-evals-usage.md` for a framework-neutral setup path.

## Output Format

For design-only tasks:

```text
Judgment: [formal eval / draft eval / smoke test / manual review only]

Why:
1. ...
2. ...

Eval design:
- Target:
- Samples:
- Grader:
- Gates:
- Report:

Next action:
1. ...
2. ...
```

For project creation tasks:

1. Create the scaffold with `scripts/create_eval_scaffold.py`.
2. Fill or copy the relevant templates.
3. Explain which files the user should edit first.
4. State whether it is ready for a real baseline or only smoke testing.

## Verification Checklist

Before finalizing:

1. The result does not contain private paths, secrets, internal project names, or customer-specific examples.
2. The eval type is labeled accurately: formal baseline, draft eval, smoke test, or manual review.
3. The grader strategy matches the task and does not overuse LLM-as-judge.
4. The sample set includes normal, boundary, failure, and high-risk cases when claiming baseline readiness.
5. The report separates results, failure types, likely causes, and next actions.
6. The output does not present unverified scores or synthetic examples as real-world proof.
