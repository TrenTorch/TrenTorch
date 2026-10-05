---
name: research-gelu-tanh
title: 'GELU: The Tanh Approximation'
tags: [research-papers, activation, gelu]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The exact GELU needs an error function, which is slow on some hardware. The paper also gives a tanh approximation that uses only multiplications, additions and tanh, and matches the exact curve closely.

### From theory to code

Implement `gelu_tanh(x)` using `0.5 x (1 + tanh(sqrt(2/pi) (x + 0.044715 x^3)))`.

### Constraints

- Must agree with the exact GELU to within `1e-3` on `[-3, 3]`.

### Hints

<details>
<summary>Hint 1</summary>

Evaluate the polynomial inside tanh first, then multiply by `0.5 * x`.

</details>

## Theory

### The simple version

The tanh form is a cheap polynomial stand-in for the Gaussian CDF. The constants were chosen so the two curves nearly coincide.

### The formula

$$\text{GELU}(x) \approx \frac{x}{2}\left(1 + \tanh\left(\sqrt{\tfrac{2}{\pi}}\,(x + 0.044715\,x^3)\right)\right)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.gelu(x, approximate='tanh')` is this approximation.

## Explanation

The approximation is what many deep learning libraries use for speed. Its error is small enough that trained models are essentially indistinguishable.
