---
name: classification-softmax-cce
title: 'Stretch: Softmax + Categorical Cross-Entropy'
tags: [classical-ml, classification, multi-class, stretch]
difficulty: Intermediate
---

## Statement

Implement:

```python
def softmax(Z: np.ndarray) -> np.ndarray:
    """Z: shape (n_samples, n_classes). Rows sum to 1."""

def cce_loss(P: np.ndarray, y_indices: np.ndarray) -> float:
    """P: shape (n_samples, n_classes) from softmax. y_indices: integer class index per sample."""
```

## Theory

```text
softmax(z)_i = exp(z_i) / Σ_j exp(z_j)
L = -log(p_correct_class)
```

With `K=2` classes, softmax + CCE reduces mathematically to sigmoid + BCE — the same idea generalized.

## Explanation

`Z - np.max(Z, axis=1, keepdims=True)` before exponentiating is the standard numerical-stability trick: subtracting each row's max shifts the largest value in that row to exactly `0` before `exp()`, so the largest term becomes `exp(0)=1` instead of risking `exp(1000)` overflowing — and because it's subtracted from every entry in the row equally, the softmax ratio (and therefore the final probabilities) is mathematically unchanged.

`P[np.arange(n), y_indices]` is fancy indexing that pulls exactly one column-per-row (the correct class's probability for each sample) — a much easier bug to introduce than it looks, since a plain `P[:, y_indices]` would instead select those columns for _every_ row.
