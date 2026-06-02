# Support Triage Rubric

## Target

Support request triage prompt.

## Decision

Decide whether the prompt can enter limited workflow testing.

## Dimensions

### 1. Label Correctness

- Pass: The output matches the approved label.
- Partial: The output identifies the right intent but adds extra words.
- Fail: The output uses the wrong label.

### 2. Format Stability

- Pass: The output is exactly one allowed label.
- Partial: The output includes one allowed label plus extra text.
- Fail: The output contains no allowed label or multiple labels.

### 3. Ambiguity Handling

- Pass: Ambiguous account/payment cases route to the first-review owner defined in the sample note.
- Partial: The output is plausible but not aligned with the expected route.
- Fail: The output invents advice or bypasses routing.
