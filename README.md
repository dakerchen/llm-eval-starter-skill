# LLM Eval Starter Skill

A starter kit for turning ad-hoc AI quality checks into a repeatable evaluation package.

Use it when you need to answer one question clearly: is this prompt, model, agent, RAG flow, or workflow good enough to ship?

| You want to... | This repo gives you... |
| --- | --- |
| define the decision | an intake checklist and success standard |
| build test cases | smoke and regression samples |
| judge the output | a rubric and deterministic checker |
| review the result | a baseline report and failure summary |
| run the eval | an OpenAI Evals-compatible scaffold or a local runner |

This project does not vendor OpenAI Evals or any other eval framework. It provides the assets and helper scripts you need to run your own eval loop.

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

- Decide whether an AI behavior is ready to ship.
- Compare prompt, model, agent, RAG, or workflow versions.
- Turn real examples into a reusable eval set.
- Produce a report that separates results, failures, causes, and next steps.

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
