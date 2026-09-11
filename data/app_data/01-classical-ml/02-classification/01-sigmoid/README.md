---
name: classification-sigmoid
title: Sigmoid Function
tags: [classical-ml, classification, activations]
difficulty: Beginner
---

## Statement

Implement:

```python
def sigmoid(z: np.ndarray) -> np.ndarray:
    """
    z: any shape of real numbers.
    Returns elementwise sigmoid, same shape as z, values strictly in (0, 1).
    """
```

Your function should:

1. Work elementwise on arrays of any shape.
2. Never overflow or return `nan`, even for very large `|z|`.
3. Return exactly `0.5` when `z = 0`.

## Theory

Linear Regression's hypothesis, `Xw + b`, can output any real number. A probability has to live strictly between 0 and 1.

```text
sigmoid(z) = 1 / (1 + exp(-z))
z (any real number) → sigmoid → probability between 0 and 1
```

- very negative `z` → probability near 0
- very positive `z` → probability near 1
- `z = 0` → probability exactly 0.5

## Explanation

`np.clip(z, -500, 500)` exists purely to stop `exp(-z)` from overflowing to `inf` for extreme inputs — `exp(500)` is already astronomically larger than any float can represent usefully, so clipping there changes nothing about the _output_ (still correctly saturates to ~0 or ~1) while preventing a `RuntimeWarning`/`nan`. The clip bound is intentionally far from where sigmoid's output actually changes (which happens within roughly `[-10, 10]`), so it never affects real behavior, only guards the exponential.
