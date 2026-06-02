# Eval Intake

## 1. Evaluation Target

- Target type: prompt
- Target name: support request triage prompt
- Target version: dev.v0
- Owner: product / support operations

## 2. Decision

- What decision will this eval support? Whether the triage prompt is ready for a limited workflow test.
- What happens if the target fails? Keep manual routing and refine labels or prompt instructions.
- Is this a release gate, regression check, comparison, or exploratory review? Smoke test.

## 3. Success Standard

- Pass: Output exactly one allowed label.
- Partial pass: Correct intent but wrong label format.
- Fail: Wrong label or extra explanation.
- Must-block issues: Invalid label, multi-label output, unsupported advice.
- Must-review issues: Ambiguous account and billing cases.

## 4. Samples

- Source: synthetic examples for public demo
- Count: 3
- Human-approved: no
- Covers normal cases: yes
- Covers boundary cases: yes
- Covers known failures: no
- Covers high-risk cases: no

## 5. Grader

- Deterministic checks: exact label match
- Exact/reference match: yes
- Rubric scoring: no
- LLM-as-judge needed: no
- Human spot-check plan: review all failures manually

## 6. Report

- Audience: product and support operations
- Decision deadline: none
- Sensitive details to remove: customer data and account details
- Output format: Markdown

## Gate Decision

- Ready for formal baseline: no
- Current level: smoke test
- Missing information: real historical support samples and approved label policy
