---
name: dl-core-swish
title: Swish (SiLU) fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-gelu` replaced ReLU's hard on/off gate with a probabilistic one built from the Gaussian CDF. That's one way to build a "self-gated" activation, where the input decides its own fate, but it's not the only one. Swish reaches the same kind of smooth, self-gating behavior using a function this track has already implemented from scratch: `02-sigmoid`.

Instead of asking "how likely is `x` to be worth keeping" via a Gaussian, Swish asks the same question via a sigmoid: `sigmoid(x)` is already a number between `0` and `1` that grows with `x`, so using it directly as the "how much to let through" gate is a natural, cheaper alternative to GELU's Gaussian CDF. This is why Swish (Google Brain's name for it) and SiLU (PyTorch's name) are the exact same function under two names, they're built from the exact building block Swish's name describes: a **si**gmoid **l**inear **u**nit.

### From theory to code

Theory writes Swish as `x` scaled by `sigmoid(x)`, using the provided `_sigmoid` helper (the same clipped, overflow-safe formula from `02-sigmoid`). Implement `swish_forward(x)` directly from that, then `swish_backward(grad_output, x)` from the product-rule derivative Theory works out, reusing `02-sigmoid`'s own derivative as one term.

### Constraints

- `x`: any shape, elementwise operation.
- Use the provided `_sigmoid` helper rather than re-deriving a raw `1 / (1 + exp(-x))`.
- `swish_backward(grad_output, x)` receives the original input `x`, not `swish_forward(x)`'s output, same requirement as `05-gelu`.
- One vectorized expression per function, no explicit loop over elements.
- Neither function modifies `x` or `grad_output` in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute `s = _sigmoid(x)` once and reuse it, it's needed for the forward output and it's also the building block for every term in the backward pass.

</details>

<details>
<summary>Hint 2</summary>

`swish_backward` needs `02-sigmoid`'s own derivative, `s * (1 - s)`, as one piece of a larger expression, not as the whole answer.

</details>

<details>
<summary>Hint 3</summary>

The full local derivative is `s + x * s * (1 - s)`: the first term comes from differentiating the `x` factor (treating `sigmoid(x)` as constant), the second from differentiating `sigmoid(x)` itself (treating `x` as constant) via the product rule.

</details>

## Theory

### The simple version

Picture the same "how much of you gets through the door" gate as `05-gelu`, except the bouncer now uses a sigmoid curve instead of a bell-curve area to decide the fraction to admit. Both bouncers behave almost identically in spirit, smooth, self-gating, and slightly ungenerous (a small negative output) to inputs a little below zero, but this one's decision rule is built from a function already on the shelf: sigmoid.

### The formula

```text
Swish(x) = x * sigmoid(x)
```

Differentiating with the product rule, letting `s = sigmoid(x)`:

```text
d/dx Swish(x) = s + x * s * (1 - s)
```

using `d/dx sigmoid(x) = sigmoid(x) * (1 - sigmoid(x))`, `02-sigmoid`'s own backward formula, reused here as one term of a larger derivative.

Like GELU, Swish is not monotonic: for small negative `x` (around `-1.28`), `sigmoid(x)` is still meaningfully positive while `x` itself is negative, so their product dips below `0` before climbing back toward `0` as `x -> -inf`. Because of that, the saved output alone can't tell you the local slope, `swish_backward` needs the original `x` (to recompute `sigmoid(x)`), not just the forward result.

### How PyTorch actually implements this

`torch.nn.functional.silu(x)` is PyTorch's name for this exact function, Swish and SiLU are not two related activations, they're the same formula. `tests.py` bakes in reference values generated once, offline, from real `torch.nn.functional.silu` forward and backward passes.

## Explanation

`swish_forward` computes `_sigmoid(x)` (the same clipped, numerically stable formula `02-sigmoid` uses) and returns `x * _sigmoid(x)`, the definition from Theory.

`swish_backward` recomputes `s = _sigmoid(x)`, builds `local_grad = s + x * s * (1.0 - s)` (Theory's product-rule derivative, with `s * (1 - s)` as the reused sigmoid-derivative term), and returns `grad_output * local_grad`.
