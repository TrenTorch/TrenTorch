---
name: classification-decision-boundary
title: Decision Boundary / Thresholding
tags: [classical-ml, classification, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sigmoid produces a continuous confidence, but an application often needs a discrete class. Thresholding turns every probability into the label convention used by the rest of the classifier while allowing a caller to choose a stricter or looser cutoff.

### From theory to code

Implement `predict_labels(p, threshold=0.5)` with one vectorized comparison. Theory states which side of the boundary includes an exact tie.

### Constraints

- `p` may be any array shape; return labels of exactly that shape.
- Return integer `0` and `1` values, not a Boolean array.
- Use `threshold=0.5` by default and honor a supplied threshold.
- A probability exactly equal to the threshold is positive.
- Do not use loops or modify `p`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

A NumPy comparison already returns one Boolean result per element.

</details>

<details><summary>Hint 2</summary>

Use the inclusive comparison, then convert the Boolean result to an integer dtype.

</details>

## Theory

### The simple version

A threshold is a decision line: confidence at or beyond the line counts as positive; confidence below it counts as negative.

### The formula

```text
label = (p >= threshold).astype(int)
```

The inclusive side is intentional: `p == threshold` maps to `1`.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch tensor comparisons such as `p >= threshold` produce a Boolean tensor, which can be converted to an integer dtype for labels.

## Explanation

The single expression `(p >= threshold)` is vectorized and preserves `p`'s shape. The `>=` includes the exact boundary, matching the tested `0.5` case. `.astype(int)` changes NumPy's Boolean result into the required integer labels without changing the array layout.
