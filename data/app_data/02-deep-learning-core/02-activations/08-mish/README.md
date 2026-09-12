---
name: dl-core-mish
title: Mish fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def mish_forward(x) -> np.ndarray: ...
def mish_backward(grad_output, x) -> np.ndarray: ...
```

Mirrors `torch.nn.functional.mish`. Like `05-gelu`/`06-swish`, `mish_backward` takes the original input `x`.

## Theory

Mish is the last self-gated activation in this track, in the same family as GELU and Swish, and is built by composing two functions this track has already covered:

```text
Mish(x) = x * tanh(softplus(x))
```

where `softplus(x) = ln(1 + exp(x))` is a smooth approximation of ReLU (it has no kink at `0`, and `softplus(x) -> x` as `x -> +inf`, `softplus(x) -> 0` as `x -> -inf`). Mish gates its input `x` by `tanh` of that smoothed-ReLU value, giving it the same overall shape as GELU and Swish: smooth, unbounded above, and slightly negative for a small range of negative `x`.

Differentiating with the product and chain rules, letting `sp = softplus(x)` and `t = tanh(sp)`:

```text
d/dx Mish(x) = t + x * (1 - t^2) * sigmoid(x)
```

This reuses two derivatives this track already derived: `d/dx softplus(x) = sigmoid(x)` (softplus is itself the antiderivative of sigmoid) and `d/dt tanh(t) = 1 - tanh(t)^2` (`03-tanh`'s own backward formula), chained together. As with GELU and Swish, Mish is not monotonic, so this derivative needs the original `x`, not just the saved output.

## Explanation

`mish_forward` computes `softplus(x)` via the numerically stable `np.logaddexp(0.0, x)` (avoids `exp` overflow the same way `04-softmax`'s row-max shift does), takes `tanh` of that, and multiplies by `x`.

`mish_backward` recomputes `t = tanh(softplus(x))` and `sigmoid(x)`, combines them into `t + x * (1 - t**2) * sigmoid(x)` (Theory's chained derivative), and multiplies by `grad_output`.
