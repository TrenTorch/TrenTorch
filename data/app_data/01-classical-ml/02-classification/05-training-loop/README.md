---
name: classification-training-loop
title: Full Training Loop
tags: [classical-ml, classification, training-loop]
difficulty: Intermediate
---

## Statement

Implement:

```python
def train_logistic_regression(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float]:
    """
    Returns final_w, final_b.
    """
```

Reuse `sigmoid` and `bce_grad` rather than reimplementing their logic.

## Theory

Identical training-loop shape to Linear Regression, hypothesis and loss swapped:

```text
initialize w, b → z = Xw+b → p = sigmoid(z) → loss = BCE(p, y) → gradient → update → repeat
```

## Explanation

Computes `z = X @ w + b` and `p = sigmoid(z)` inline rather than through a separate `linear_forward` call — `sigmoid` needs the raw score `z` as an intermediate value it can reuse conceptually, and keeping both visible here makes the forward pass's two stages (linear score, then squash) explicit rather than hidden behind one function name.

Note on the `_load` import: dev-repo convenience so this file is independently runnable via `pytest`. In the actual student-facing Pyodide session, `sigmoid`/`bce_grad` are already defined in the same running session from earlier questions in this track.
