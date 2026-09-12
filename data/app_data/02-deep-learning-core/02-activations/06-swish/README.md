---
name: dl-core-swish
title: Swish (SiLU) fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def swish_forward(x) -> np.ndarray: ...
def swish_backward(grad_output, x) -> np.ndarray: ...
```

- Swish and SiLU (Sigmoid Linear Unit) are the same function, `torch.nn.functional.silu` is PyTorch's name for it.
- Like `05-gelu`, `swish_backward` takes the original input `x`, not the saved output.

## Theory

Swish (introduced by a Google Brain search over activation functions, also independently called SiLU) is:

```text
Swish(x) = x * sigmoid(x)
```

It shares GELU's overall shape: smooth everywhere, unbounded above, and, critically, **not monotonic**. For `x` slightly negative (around `x = -1.28`), `sigmoid(x)` is still meaningfully positive while `x` itself is negative, so their product dips below `0` before climbing back toward `0` as `x -> -inf`. This is the same "self-gating" idea GELU implements with a Gaussian CDF instead of a sigmoid: the input gates itself by (roughly) how likely it is to be "on."

Differentiating with the product rule, letting `s = sigmoid(x)`:

```text
d/dx Swish(x) = s + x * s * (1 - s)
```

using `d/dx sigmoid(x) = sigmoid(x) * (1 - sigmoid(x))`, `02-sigmoid`'s own backward formula, reused here as one term of a larger derivative. As with GELU, because Swish is not monotonic, the saved output alone cannot tell you the local slope, the backward pass needs the original `x` (to recompute `sigmoid(x)`), not just the forward result.

## Explanation

`swish_forward` computes `sigmoid(x)` via the provided `_sigmoid` helper (the same clipped, numerically stable formula from `02-sigmoid`) and multiplies by `x`.

`swish_backward` recomputes `s = sigmoid(x)`, combines it into `s + x * s * (1 - s)` (Theory's product-rule derivative), and multiplies by `grad_output`.
