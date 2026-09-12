---
name: dl-core-mish
title: Mish fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-gelu` and `06-swish` each build a self-gated activation from a different "how much to let through" curve, a Gaussian CDF for one, a sigmoid for the other. Mish is the third and last self-gated activation in this track, and it takes a different route to the same idea: instead of gating `x` directly with a probability curve, it first smooths `x` itself, then gates the smoothed version.

Concretely, Mish starts from `softplus`, a version of ReLU with the kink at `0` sanded off, and squashes that through `tanh` before multiplying back into `x`. The result is, once again, smooth everywhere, unbounded for large positive `x`, and slightly negative for a narrow range of negative inputs, the same family resemblance GELU and Swish share, built here entirely out of two functions this track already has in place: `03-tanh` and the softplus function underlying `02-sigmoid`.

### From theory to code

Theory composes two already-familiar pieces, `softplus` (provided as `_softplus`) and `tanh`, then gates `x` with the result. Implement `mish_forward(x)` as that direct composition, and `mish_backward(grad_output, x)` from the chained product-rule derivative Theory works out, which reuses `03-tanh`'s own backward formula and `_sigmoid` as pieces of a larger expression.

### Constraints

- `x`: any shape, elementwise operation.
- Use the provided `_softplus` (numerically stable `np.logaddexp(0, x)`, not a literal `log(1 + exp(x))`) and `_sigmoid` helpers rather than re-deriving them.
- `mish_backward(grad_output, x)` receives the original input `x`, not `mish_forward(x)`'s output, same requirement as `05-gelu` and `06-swish`.
- One vectorized expression per function, no explicit loop over elements.
- Neither function modifies `x` or `grad_output` in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute `_softplus(x)` first, then `np.tanh` of that result, that intermediate value (call it `sp`, or its `tanh`, call it `t`) is the piece both forward and backward build on.

</details>

<details>
<summary>Hint 2</summary>

`mish_backward` needs `03-tanh`'s own derivative pattern, `1 - tanh(...)^2`, applied to `t = tanh(softplus(x))`, as one factor, not as the whole answer.

</details>

<details>
<summary>Hint 3</summary>

The full local derivative is `t + x * (1 - t**2) * sigmoid(x)`: the first term comes from differentiating the `x` factor (treating the `tanh(softplus(x))` gate as constant), the second from differentiating the gate itself, chaining `03-tanh`'s derivative through `softplus`'s own derivative, which happens to just be `sigmoid(x)`.

</details>

## Theory

### The simple version

GELU and Swish each gate `x` with a probability-shaped curve evaluated directly at `x`. Mish instead first runs `x` through a smoothed, kink-free version of ReLU, then squashes *that* through an S-shaped curve before using it as the gate. It's one extra step of smoothing before the same self-gating idea kicks in, and it lands in the same family: smooth everywhere, unbounded above, and dipping slightly negative for a narrow band of negative inputs.

### The formula

```text
Mish(x) = x * tanh(softplus(x))
```

where `softplus(x) = ln(1 + exp(x))`. Differentiating with the product and chain rules, letting `sp = softplus(x)` and `t = tanh(sp)`:

```text
d/dx Mish(x) = t + x * (1 - t^2) * sigmoid(x)
```

This reuses two derivatives this track already derived: `d/dx softplus(x) = sigmoid(x)` (softplus is itself the antiderivative of sigmoid) and `d/dt tanh(t) = 1 - tanh(t)^2` (`03-tanh`'s own backward formula), chained together. Like GELU and Swish, Mish is not monotonic, so this derivative needs the original `x`, not just the saved output.

### How PyTorch actually implements this

`torch.nn.functional.mish(x)` computes exactly this composition. `tests.py` bakes in reference values generated once, offline, from real `torch.nn.functional.mish` forward and backward passes.

## Explanation

`mish_forward` computes `_softplus(x)` (the numerically stable `np.logaddexp(0.0, x)`, avoiding `exp` overflow the same way `04-softmax`'s row-max shift does), takes `np.tanh` of that, and returns `x * np.tanh(_softplus(x))`, the definition from Theory.

`mish_backward` recomputes `t = np.tanh(_softplus(x))` and `s = _sigmoid(x)`, combines them into `local_grad = t + x * (1.0 - t**2) * s` (Theory's chained derivative), and returns `grad_output * local_grad`.
