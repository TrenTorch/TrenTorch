---
name: research-scaling-ratio
title: 'Scaling Laws: Predicting the Gain From Growth'
tags: [research-papers, transformers, llm, scaling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Scaling laws are most useful for planning. If you know the exponent, you can estimate how much loss you will save by growing the model, before you spend the compute to train it.

### From theory to code

Implement `loss_ratio_for_size_increase(factor, alpha)`, returning `factor ** (-alpha)`.

### Constraints

- `factor` is the ratio of new size to old size.

### Hints

<details>
<summary>Hint 1</summary>

Raise the factor to the power of the negated exponent.

</details>

## Theory

### The simple version

A larger exponent means each doubling saves more loss. Because the law is multiplicative, repeated growth compounds.

### The formula

$$\frac{L(kN)}{L(N)} = k^{-\alpha}$$

### How NumPy/PyTorch actually implements this

Planning spreadsheets for training runs compute this ratio directly from a fitted exponent.

## Explanation

The ratio is independent of the starting size, which is why a single exponent describes the whole range of the fit.
