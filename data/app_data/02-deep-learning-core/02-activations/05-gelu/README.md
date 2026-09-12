---
name: dl-core-gelu
title: GELU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def gelu_forward(x) -> np.ndarray: ...
def gelu_backward(grad_output, x) -> np.ndarray: ...
```

- Exact GELU (the default of `torch.nn.functional.gelu`, not the `tanh`-approximate variant).
- `gelu_backward` takes the original input `x`, not the saved output, unlike `02-sigmoid`/`03-tanh`/`04-softmax`, see Theory for why.

## Theory

GELU (Gaussian Error Linear Unit), the activation behind BERT, GPT, and most modern transformers, is defined as:

```text
GELU(x) = x * Phi(x)
```

where `Phi` is the standard normal CDF, "the probability a standard normal random variable is less than `x`." Intuitively, GELU multiplies the input by "how likely is this input to be kept," a smooth, probabilistic version of ReLU's hard "keep if positive, drop if negative" gate. Unlike ReLU, GELU is smooth everywhere (no kink at `0`) and, unlike ReLU, it is not monotonic: for small negative `x` (around `-0.75`), `GELU(x)` dips slightly below `0` before rising back toward `0` as `x -> -inf`.

`Phi` is expressed via the error function `erf`:

```text
Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))
```

Differentiating `GELU(x) = x * Phi(x)` with the product rule gives:

```text
d/dx GELU(x) = Phi(x) + x * phi(x)
```

where `phi(x) = exp(-x^2/2) / sqrt(2*pi)` is the standard normal PDF (the derivative of `Phi`).

This is why GELU's backward, uniquely in this track, needs the original input `x` rather than the saved output: because GELU dips negative and is not monotonic, two different inputs can occasionally sit near the same output value, so the output alone does not determine the local slope the way it does for a strictly monotonic function like sigmoid or tanh.

## Explanation

`gelu_forward` computes `Phi(x)` via `0.5 * (1 + erf(x / sqrt(2)))` (using the provided vectorized `math.erf`) and multiplies by `x`, exactly the definition from Theory.

`gelu_backward` computes `Phi(x)` (same formula) and `phi(x) = exp(-x^2/2) / sqrt(2*pi)`, combines them into `Phi(x) + x * phi(x)`, and multiplies by `grad_output`, the product-rule derivative from Theory.
