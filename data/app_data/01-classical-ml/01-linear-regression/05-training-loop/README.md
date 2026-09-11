---
name: linear-regression-training-loop
title: Full Linear Regression Training Loop
tags: [classical-ml, linear-regression, training-loop]
difficulty: Intermediate
---

## Statement

Implement:

```python
def train_linear_regression(
    X: np.ndarray,
    y: np.ndarray,
    lr: float,
    epochs: int
) -> tuple[np.ndarray, float]:
    """
    Train a linear regression model using gradient descent.

    Returns:
        final_w, final_b
    """
```

Your function should:

1. Initialize `w` and `b` to zero values.
2. Repeat the following for `epochs` iterations:
   - call `linear_forward()` to calculate predictions;
   - call `mse_grad()` to calculate `dw` and `db`;
   - call `gd_step()` to update `w` and `b`.
3. Return the final `w` and `b`.

Use the functions you already implemented in the earlier questions rather than reimplementing their logic inside the training loop.

## Theory

We now have every individual piece required to train the model.

Training simply means repeating the same process many times:

```text
initialize w, b
       ↓
   predict
       ↓
   calculate loss
       ↓
   calculate gradient
       ↓
   update w, b
       ↓
     repeat
```

Each repetition is called an epoch.

As training progresses, the parameters should move toward values that produce smaller prediction errors.

This is the basic training-loop pattern that will appear again and again in deep learning. Later, the model, loss, and optimizer may become much more complicated, but the structure is fundamentally the same.

## Explanation

`w = np.zeros(X.shape[1])`, not a hardcoded size — this is what lets the function work for any `n_features` without the caller passing it separately.

The loop body is `linear_forward` → `mse_grad` → `gd_step` in sequence and _nothing else_; no computation is reimplemented here, only wired together — every actual formula stays owned by the function that was already tested for it.

Note on the `_load` import at the top: that's a dev-repo convenience so this file is independently runnable via `pytest` outside the app. In the actual student-facing Pyodide session, `linear_forward`/`mse_grad`/`gd_step` are already defined in the same running session from the earlier questions in this track — a real student's version of this function calls them directly, no import needed.
