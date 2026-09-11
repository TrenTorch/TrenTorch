---
name: classification-decision-boundary
title: Decision Boundary / Thresholding
tags: [classical-ml, classification, inference]
difficulty: Beginner
---

## Statement

Implement:

```python
def predict_labels(p: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Returns integer labels (0 or 1), same shape as p.
    """
```

## Theory

```text
predict 1 if p >= threshold, else 0
```

The decision boundary is exactly where `p = 0.5`, i.e. where the raw score `z = 0` — a straight line, which is why logistic regression is a _linear_ classifier despite sigmoid being a curve.

## Explanation

`>=`, not `>` — the threshold value itself is defined to belong to the positive class by convention (matches `p == 0.5` predicting 1, which is what the "value exactly at threshold" test checks). `.astype(int)` converts NumPy's boolean array to actual integer labels rather than leaving `True`/`False`, which would compare correctly against `0`/`1` in most contexts but isn't what "returns integer labels" actually asked for.
