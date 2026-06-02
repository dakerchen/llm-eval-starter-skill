# Sample Design

Good eval samples are decision assets, not random examples.

## Sample Types

| Type | Purpose | Minimum |
|---|---|---:|
| Smoke | Verify runner and output path | 1-3 |
| Normal | Cover expected use | 3-10 |
| Boundary | Cover ambiguity, missing fields, long context, mixed intent | 3-10 |
| Failure regression | Prevent known old failures from returning | 3-20 |
| High risk | Cover safety, compliance, factuality, sensitive decisions | As needed |

## Required Fields

Each sample should include:

1. `id`
2. `input`
3. `expected` or `ideal`
4. `tags`
5. `risk`
6. `notes`

## Baseline Readiness

A sample set is not baseline-ready unless:

1. It contains real or human-approved examples.
2. It covers normal, boundary, failure, and high-risk cases.
3. Expected outputs are stable enough to grade.
4. A human owner agrees that the pass/fail criteria reflect the product decision.

If these are missing, label the set as draft or smoke only.
