# Grader Selection

Use the simplest grader that can support the decision.

## Default Priority

| Priority | Grader | Best For | Risk |
|---:|---|---|---|
| 1 | Rule check | JSON validity, required fields, enum values, citations present, refusal required | Misses semantic quality |
| 2 | Exact match | Classification, routing, fixed labels, multiple choice | Too rigid for open text |
| 3 | Reference answer | QA, extraction, summaries, grounded answers | Requires trusted references |
| 4 | Rubric scoring | Complex writing, analysis, synthesis, decision support | Needs clear criteria |
| 5 | LLM-as-judge | Semantic comparison when rules are insufficient | Can drift and must be sampled by humans |

## Strong Gates

Use strong gates when failure should block release or trigger manual review:

1. Invalid JSON or schema.
2. Missing required fields.
3. Unsafe or disallowed content.
4. Unsupported factual claims.
5. Wrong fixed label or action.
6. Tool call missing, duplicated, or called with wrong arguments.
7. Required citation absent or not linked to source material.

## Weak Gates

Use weak gates when the issue informs quality but should not automatically block:

1. Tone.
2. Readability.
3. Depth of explanation.
4. Helpfulness.
5. Style alignment.
6. Non-critical completeness.

## Rubric Pattern

Write criteria so a reviewer can decide consistently:

```text
Dimension: Source grounding
Pass: Uses only facts present in the input and cites the relevant source.
Partial: Main answer is grounded, but one minor claim lacks explicit support.
Fail: Adds an unsupported material claim or contradicts the source.
```

Avoid vague criteria:

```text
Good quality, clear logic, natural language.
```

## LLM-as-Judge Rules

Use LLM-as-judge only when:

1. The target output is semantic or open-ended.
2. A human-readable rubric exists.
3. You can sample judge decisions manually.
4. The judge prompt and model version are recorded.

Do not use LLM-as-judge as the only gate for high-risk decisions.
