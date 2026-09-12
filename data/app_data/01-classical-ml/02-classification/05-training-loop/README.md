---
name: classification-training-loop
title: Full Training Loop
tags: [classical-ml, classification, training-loop]
difficulty: Intermediate
---

## Statement

Implement:

```python
def train_logistic_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    input:  shape (batch_size, in_features)
    target: shape (batch_size,), 0 or 1 per sample

    Returns:
        weight: shape (1, in_features)
        bias: shape (1,)
    """
```

Reuse `01-hypothesis-function`'s `linear`, `01-sigmoid`'s `sigmoid`, `03-bce-gradient`'s `bce_gradient`, and Linear Regression's `04-gd-step`'s `gd_step`, rather than reimplementing any of their logic.

## Theory

Identical training-loop shape to Linear Regression, hypothesis and loss swapped:

```text
initialize weight, bias → z = linear(input, weight, bias) → p = sigmoid(z) → loss = BCE(p, target) → gradient → update → repeat
```

The update step itself, `weight - lr * grad_weight`, doesn't care whether the loss came from MSE or BCE, `04-gd-step`'s `gd_step` is exactly as reusable here as it was for Linear Regression. That reuse is only possible because both tracks settled on the same `weight`/`bias` shape convention, `(1, in_features)` / `(1,)`, never a bare `(in_features,)` vector and a Python `float`.

## Explanation

`weight = np.zeros((1, input.shape[1]))`, `bias = np.zeros(1)`, and `target_2d = target.reshape(-1, 1)` mirror Linear Regression's `05-training-loop` exactly, reshape the natural `(batch_size,)` label vector once, up front, then every downstream call is shape-safe.

`p = sigmoid(linear(input, weight, bias))` makes the forward pass's two stages explicit: `linear` produces the raw score, `sigmoid` squashes it to a probability, matching the `z → p` split Theory describes.

The loop body is `linear` → `sigmoid` → `bce_gradient` → `gd_step`, in sequence, and nothing else. `gd_step` comes from Linear Regression's track, not reimplemented here, the whole point of settling on one shared `weight`/`bias` convention across tracks.
