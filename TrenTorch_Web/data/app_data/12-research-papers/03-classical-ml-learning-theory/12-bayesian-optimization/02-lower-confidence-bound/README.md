---
name: research-bo-lower-confidence-bound
title: 'Bayesian Optimization: Lower Confidence Bound'
tags: [research-papers, classical-ml, bayesian-optimization, hyperparameters]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A simple acquisition rule is to try the point with the lowest optimistic estimate: the predicted mean minus kappa times its uncertainty. Points with high uncertainty look better, which drives exploration.

### From theory to code

Implement `lower_confidence_bound(mu, sigma, kappa)`, returning `mu - kappa * sigma`.

### Constraints

- For minimization, pick the candidate with the smallest value.

### Hints

<details>
<summary>Hint 1</summary>

Subtract `kappa` times `sigma` from `mu`, element-wise.

</details>

## Theory

### The simple version

A candidate can be attractive either because its mean is low (exploitation) or because it is uncertain (exploration). Kappa sets the trade-off.

### The formula

$$\text{LCB}(x) = \mu(x) - \kappa\,\sigma(x)$$

### How NumPy/PyTorch actually implements this

Acquisition functions in optimization libraries include this rule as an option alongside expected improvement.

## Explanation

This is the minimization form of the upper confidence bound used in bandit problems.
