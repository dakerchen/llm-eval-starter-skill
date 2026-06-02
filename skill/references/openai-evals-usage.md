# OpenAI Evals Usage Boundary

This skill can create starter files for OpenAI Evals-style projects, but it does not include OpenAI Evals itself.

## Role Split

| Layer | Role |
|---|---|
| Skill | Designs the eval scope, samples, grader strategy, and report |
| OpenAI Evals | Runs registered evals and writes logs |
| Templates | Provide starter YAML, JSONL, rubric, and report files |
| Scripts | Scaffold local files and summarize JSONL logs |

## First Run Check

Before designing a formal run:

```bash
python3 skill/scripts/detect_openai_evals.py
```

If `oaieval` is found, inspect the local installation and follow the local project's registry layout.

If it is not found, ask the user to install OpenAI Evals or provide their eval runner. Do not guess private paths.

## Minimal Run Principle

Start with the smallest possible eval:

1. One or two samples.
2. One simple grader.
3. One model or target version.
4. One output log.

Only scale after the runner, data path, credentials, and log parsing are confirmed.

## What To Record

Each report should record:

1. Target version.
2. Sample set version.
3. Grader strategy and version.
4. Runner command.
5. Date/time.
6. Result summary.
7. Failure types.

## Common Mistakes

1. Treating a smoke run as a quality baseline.
2. Comparing two prompt versions while also changing the sample set.
3. Using LLM-as-judge for strict schema or enum validation.
4. Reporting only average score without failure examples.
5. Copying a framework repository into a skill package.
