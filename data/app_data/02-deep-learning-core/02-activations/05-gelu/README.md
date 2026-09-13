---
name: dl-core-gelu
title: GELU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-relu`'s gate is binary: a neuron's input either survives untouched (`x > 0`) or gets zeroed out completely (`x <= 0`), decided purely by sign. That's a crude rule. A value of `x = 0.01` and a value of `x = -0.01` sit almost on top of each other, yet ReLU treats one as "fully kept" and the other as "fully discarded."

GELU replaces that hard switch with a soft, probabilistic one: instead of asking "is `x` positive?", it asks "how likely is `x` to be a value worth keeping?" and scales `x` down by that likelihood. Values far from zero (very positive or very negative) get a decisive answer, close to "keep everything" or "keep nothing." Values near zero get partial credit. This smoother gating is one reason GELU, not ReLU, became the default activation inside BERT, GPT, and most transformer architectures built after them.

### From theory to code

Theory expresses "how likely is `x` to be worth keeping" as the standard normal CDF, `Phi(x)`, and defines GELU as `x` scaled by `Phi(x)`. `Phi` itself is written in terms of the error function `erf`, which the file already imports and vectorizes as `_erf`.

Implement `gelu_forward(x)` using `_erf` to build `Phi(x)`, then `gelu_backward(grad_output, x)` using the product-rule derivative Theory derives. Note the backward signature: it takes the original `x`, not a saved output, the "why" is covered in Theory.

### Constraints

- `x`: any shape, elementwise operation.
- Use the provided `_erf` (a vectorized `math.erf`) rather than any other error-function implementation.
- `gelu_backward(grad_output, x)` receives the original input `x`, not `gelu_forward(x)`'s output, unlike `02-sigmoid`, `03-tanh`, and `04-softmax`.
- One vectorized expression per function, no explicit loop over elements.
- Neither function modifies `x` or `grad_output` in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`Phi(x)`, the standard normal CDF, shows up in both `gelu_forward` and `gelu_backward`. Write it once as its own expression using `_erf`, `_SQRT_2`, and it becomes a shared building block for both functions.

</details>

<details>
<summary>Hint 2</summary>

The backward pass needs the standard normal _density_ `phi(x)` (lowercase), not just `Phi(x)` (uppercase). They're different functions: `phi(x) = exp(-x^2/2) / sqrt(2*pi)`, `_SQRT_2PI` is already provided for exactly this.

</details>

<details>
<summary>Hint 3</summary>

`gelu_backward` combines `Phi(x)` and `x * phi(x)` by addition, then multiplies the sum by `grad_output`. That's the whole function, no other terms are needed.

</details>

## Theory

### The simple version

Imagine a bouncer at a door who doesn't just check "are you on the list" (ReLU's yes/no), but instead looks at how closely you resemble someone who belongs, and lets a proportional fraction of you through. Someone who clearly belongs gets waved through in full. Someone who clearly doesn't gets stopped entirely. Someone borderline gets... partially let in, GELU's odd but real behavior of producing a small negative output for inputs a little below zero.

### The formula

```text
GELU(x) = x * Phi(x)
```

where `Phi` is the standard normal CDF, `Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))`. Because `GELU` is a product of `x` and a smooth function of `x`, differentiating with the product rule gives:

```text
d/dx GELU(x) = Phi(x) + x * phi(x)
```

where `phi(x) = exp(-x^2/2) / sqrt(2*pi)` is the standard normal PDF (the derivative of `Phi`).

GELU is not monotonic: for small negative `x` (around `-0.75`), `GELU(x)` dips slightly below `0` before rising back toward `0` as `x -> -inf`. That's why `gelu_backward` needs the original input `x` rather than the saved forward output, unlike a strictly monotonic function like sigmoid or tanh, the output value alone doesn't pin down which `x` produced it, or what the local slope was there.

### How PyTorch actually implements this

`torch.nn.functional.gelu(x, approximate='none')`, the default, computes exactly this erf-based form (there's also an `approximate='tanh'` variant that swaps in a `tanh`-based approximation for speed, not implemented here). `tests.py` bakes in reference values generated once, offline, from real `torch.nn.functional.gelu` forward and backward passes.

## Explanation

`gelu_forward` builds `Phi(x)` as `0.5 * (1.0 + _erf(x / _SQRT_2))` and returns `0.5 * x * (1.0 + _erf(x / _SQRT_2))`, the definition from Theory applied directly with the provided vectorized `_erf`.

`gelu_backward` recomputes `cdf = 0.5 * (1.0 + _erf(x / _SQRT_2))` (the same `Phi(x)`) and `pdf = np.exp(-0.5 * x**2) / _SQRT_2PI` (`phi(x)`), combines them into `local_grad = cdf + x * pdf`, exactly Theory's product-rule derivative, and returns `grad_output * local_grad`, the chain rule applied to that local slope.
