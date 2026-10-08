---
name: research-catboost-target-statistic
title: 'CatBoost: The Target Statistic Formula'
tags: [research-papers, classical-ml, boosting, catboost]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A category seen only once or twice gives an unreliable mean. Blending that mean with a prior, weighted by a, keeps the encoding stable when data is sparse.

### From theory to code

Implement `target_statistic(sum_y, count, prior, a)`, returning `(sum_y + a * prior) / (count + a)`.

### Constraints

- With no history the statistic equals the prior.

### Hints

<details>
<summary>Hint 1</summary>

Add the prior's pseudo-count to the label sum and the denominator.

</details>

## Theory

### The simple version

The prior acts like `a` extra samples with label `prior`. Large categories are dominated by their own data, while rare ones are dominated by the prior.

### The formula

$$\hat x = \frac{\sum y + a\,p}{n + a}$$

### How NumPy/PyTorch actually implements this

The formula is the building block of CatBoost's ordered statistics; the ordering is handled by the caller.

## Explanation

This is the same smoothing used in Bayesian estimates of a Bernoulli mean with a conjugate prior.
