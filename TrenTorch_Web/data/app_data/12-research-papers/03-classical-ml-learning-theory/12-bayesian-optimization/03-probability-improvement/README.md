---
name: research-bo-probability-improvement
title: 'Bayesian Optimization: Probability of Improvement'
tags: [research-papers, classical-ml, bayesian-optimization, hyperparameters]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Probability of improvement is the simplest Bayesian optimization rule. It scores a candidate by the chance that its true value lands below the best so far. It ignores how much the improvement would be, which is the weakness expected improvement fixes.

### From theory to code

Implement `probability_of_improvement(mu, sigma, best)` for minimization, returning the standard normal CDF of `(best - mu) / sigma`.

### Constraints

- `sigma` is positive.

### Hints

<details>
<summary>Hint 1</summary>

Compute `z = (best - mu) / sigma` and return `Phi(z)` using `math.erf`.

</details>

## Theory

### The simple version

A candidate that is almost surely a little better scores as high as one that is very likely to be much better. This indifference to size is why expected improvement is usually preferred.

### The formula

$$\text{PI}(x) = \Phi\!\left(\frac{f^* - \mu(x)}{\sigma(x)}\right)$$

### How NumPy/PyTorch actually implements this

Many libraries expose this as an alternative acquisition function for tuning comparisons.

## Explanation

The expression is the first term of expected improvement, without the magnitude weighting.
