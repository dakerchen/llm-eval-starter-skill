# LLM Eval Starter Skill

A small, open-source-ready Skill for creating task-specific LLM evaluation packages.

It helps teams move from "the output feels better" to a repeatable loop:

1. Define the target behavior.
2. Create smoke and regression samples.
3. Choose a grader strategy.
4. Run a small baseline.
5. Report failure types and next actions.

This project does not vendor OpenAI Evals or any other eval framework. It provides a reusable Skill, templates, and helper scripts that can work with OpenAI Evals or a local runner.

## Install

```bash
pip install -e .
```

## Local Commands

- `llm-eval-starter-validate`
- `llm-eval-starter-scaffold`
- `llm-eval-starter-detect`
- `llm-eval-starter-summarize`
- `llm-eval-starter-build-release`

## What It Is For

- Prompt regression checks.
- Model or prompt version comparison.
- Agent, RAG, or workflow output QA.
- Small eval scaffolds before investing in a full evaluation system.
- Product-facing quality reports that separate results, failures, causes, and next steps.

## What It Is Not

- A general model benchmark.
- A replacement for human review.
- A production monitoring system.
- A copy of OpenAI Evals.
- A guarantee that a few examples are a real quality baseline.

## Repository Layout

```text
llm-eval-starter-skill/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── SECURITY.md
├── skill/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── assets/templates/
│   └── scripts/
├── examples/support-triage/
├── scripts/validate_public_package.py
└── dist/
```

The installable Skill is the `skill/` folder. The rest of the repository is public documentation, examples, and release tooling.

## Quick Start

Create a starter eval folder:

```bash
llm-eval-starter-scaffold support-triage --out examples
```

Check whether OpenAI Evals is available in your current shell:

```bash
llm-eval-starter-detect
```

Summarize a JSONL eval result:

```bash
llm-eval-starter-summarize path/to/results.jsonl
```

## Recommended Workflow

1. Fill `eval-intake.md`.
2. Edit `data/<name>/samples.jsonl`.
3. Define the rubric in `rubric.md`.
4. Run a smoke test with 1-3 examples.
5. Review failure examples manually.
6. Only call it a baseline after samples and rubric are human-approved.

## Release Check

Before publishing:

```bash
llm-eval-starter-validate
```

The validator checks for required files, Skill metadata, private path patterns, and obvious internal markers.

To build the release archive:

```bash
pip install -e '.[release]'
llm-eval-starter-build-release
```
