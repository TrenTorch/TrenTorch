---
name: research-scaling-power-law-loss
title: 'Scaling Laws: The Power-Law Loss'
tags: [research-papers, transformers, llm, scaling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Kaplan et al. (2020) found that language model loss falls as a power law in model size, dataset size and compute, across many orders of magnitude. A power law is a straight line on a log-log plot, which is why it is easy to fit and extrapolate.

### From theory to code

Implement `power_law_loss(N, N_c, alpha)`, which returns `(N_c / N) ** alpha`.

### Constraints

- Works on scalars and arrays.

### Hints

<details>
<summary>Hint 1</summary>

Divide the scale by the size and raise to the exponent.

</details>

## Theory

### The simple version

Doubling the parameters multiplies the loss by a fixed factor, `2 ** -alpha`, no matter where you start. That regularity is what made the scaling laws predictive.

### The formula

$$L(N) = \left(\frac{N_c}{N}\right)^{\alpha_N}$$

### How NumPy/PyTorch actually implements this

Plotting `L(N)` on log-log axes gives a straight line, which is how the paper presents the fits.

## Explanation

The function is a direct power law; the constant `N_c` sets where the curve crosses one, and `alpha` sets its slope on log-log axes.
