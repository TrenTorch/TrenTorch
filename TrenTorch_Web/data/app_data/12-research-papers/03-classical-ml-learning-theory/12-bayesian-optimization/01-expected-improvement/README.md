---
name: research-ei-expected-improvement
title: 'Bayesian Optimization: Expected Improvement'
tags: [research-papers, classical-ml, bayesian-optimization, hyperparameters]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Bayesian optimization (Frazier, 2018) tunes expensive functions, such as hyperparameters, by fitting a surrogate model with uncertainty and choosing the next point to try. Expected improvement scores each candidate by how much it is expected to beat the best result so far.

### From theory to code

Implement `expected_improvement(mu, sigma, best)` for a minimization problem, using the standard normal CDF and density.

### Constraints

- `sigma` is positive.

### Hints

<details>
<summary>Hint 1</summary>

Compute `z = (best - mu) / sigma`, then combine `(best - mu) * Phi(z)` with `sigma * phi(z)`.

</details>

## Theory

### The simple version

The first term rewards a candidate whose mean is below the current best. The second rewards uncertainty, so promising unexplored regions are not ignored.

### The formula

$$\text{EI}(x) = (f^* - \mu)\,\Phi(z) + \sigma\,\phi(z), \qquad z = \frac{f^* - \mu}{\sigma}$$

### How NumPy/PyTorch actually implements this

BoTorch and scikit-optimize compute the same expression for their acquisition functions.

## Explanation

This is the closed form for a Gaussian-process surrogate, where the posterior at each point is a normal distribution.
