---
name: ensembles-error-ambiguity-decomposition
title: Error-ambiguity decomposition
tags: [classical-ml, ensembles, diversity]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Why does averaging many models help? The error-ambiguity decomposition gives an exact answer for regression: the averaged ensemble's error equals the models' average error minus how much the models disagree with each other. Disagreement is only useful when the models are still individually accurate.

### From theory to code

Implement `ambiguity_decomposition(predictions, target)` for a simple-average ensemble of regressors, returning the ensemble error, the mean individual error and the ambiguity. Errors are mean squared errors.

### Constraints

- `predictions` has shape `(n_models, n_samples)`; `target` has shape `(n_samples,)`.
- The ensemble prediction is the unweighted mean of the models.
- Return a tuple of three Python floats: `(ensemble_error, mean_individual_error, ambiguity)`.
- Compute all three directly from their definitions, not from the identity.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Ensemble error is the squared error of the averaged prediction. Mean individual error averages the squared error over models _and_ samples.

</details>

<details><summary>Hint 2</summary>

Ambiguity is the average squared distance between each model's prediction and the ensemble's prediction, again over models and samples.

</details>

## Theory

### The simple version

Imagine three forecasters who all miss in different directions. Their average can be far closer to the truth than any of them, and the amount by which it improves is exactly how much they disagree.

### The formula

$$E = \bar{E} - \bar{A}$$

$$E = \overline{(H - y)^2},\quad \bar{E} = \frac{1}{T}\sum_i \overline{(h_i - y)^2},\quad \bar{A} = \frac{1}{T}\sum_i \overline{(h_i - H)^2}$$

where $H$ is the mean of the $h_i$ and the bars average over samples. Since $\bar{A} \ge 0$, the ensemble is never worse than the average member.

### How libraries implement this

This is a property of squared loss and averaging, not a library feature; it motivates diversity-generating methods such as bagging and random feature subsets.

## Explanation

Each quantity is a one-line NumPy reduction with broadcasting over the model axis. The identity `E == E_bar - A` then holds numerically, which is also what the tests check.
