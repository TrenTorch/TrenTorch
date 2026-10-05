---
name: evaluation-mean-regressor-baseline
title: Mean regressor baseline
tags: [classical-ml, evaluation, baselines]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The regression version of the majority-class baseline predicts the same value for every example. The best constant under squared error is the training mean. A regression model should beat it, and `R-squared score` is defined so that this baseline scores exactly zero.

Implement `mean_regressor_baseline(y_train, n_samples)`, which returns an array of length `n_samples` filled with the mean of `y_train` as a float.

### Constraints

- `y_train` must not be empty: raise `ValueError`.
- The output dtype is float, even if `y_train` holds integers.
- Do not modify `y_train`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Convert `y_train` to a float array first, then take its mean.

</details>

<details>
<summary>Hint 2</summary>

`np.full(n_samples, value)` builds the constant array in one call.

</details>

## Theory

### The simple version

With no features to lean on, the least risky guess under squared error is the average of what you have seen. Any error the model makes is measured against that same yardstick.

### The formula

$$
\hat{y} = \bar{y} = \frac{1}{n} \sum_{i=1}^{n} y_i
$$

## Explanation

`mean_regressor_baseline` converts the training targets to floats, rejects an empty array, and fills the output with their mean. The float conversion keeps the output dtype consistent for integer targets.
