---
name: research-gelu-exact
title: 'GELU: The Exact Gaussian-Gated Activation'
tags: [research-papers, activation, gelu]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

ReLU gates inputs with a hard threshold at zero. GELU (Hendrycks & Gimpel, 2016) gates each input by how likely it is to be positive under a Gaussian, giving a smooth version of that decision.

### From theory to code

Implement `gelu_exact(x)`, which returns `x * Phi(x)`, where `Phi` is the standard normal cumulative distribution.

### Constraints

- Uses `math.erf`; no SciPy.

### Hints

<details>
<summary>Hint 1</summary>

`Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))`. Multiply the input by that value.

</details>

## Theory

### The simple version

Large positive inputs are almost surely kept, large negative inputs almost surely dropped, and inputs near zero are scaled smoothly. That is a soft version of ReLU's hard gate.

### The formula

$$\text{GELU}(x) = x\,\Phi(x), \qquad \Phi(x) = \frac{1}{2}\left(1 + \operatorname{erf}\left(\frac{x}{\sqrt{2}}\right)\right)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.gelu(x)` implements this exact form when `approximate='none'`.

## Explanation

`erf` is the error function; `math.erf` evaluates it on scalars, so `np.vectorize` applies it over arrays.
