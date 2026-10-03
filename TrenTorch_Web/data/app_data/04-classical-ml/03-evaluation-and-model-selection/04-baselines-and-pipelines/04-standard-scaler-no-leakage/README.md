---
name: evaluation-standard-scaler-no-leakage
title: Standard scaler without leakage
tags: [classical-ml, evaluation, preprocessing, data-leakage]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Scaling features is one of the easiest places to leak information into a model. If you compute the mean and standard deviation over the full dataset before splitting, the test set has already shaped the training features. The fix is to learn the scaling statistics from the training rows only, then apply those same numbers to the test rows, even when the test rows look different.

Implement `standard_scale_no_leakage(X_train, X_test)`, which returns `(scaled_train, scaled_test)`. Both are scaled with the per-column mean and standard deviation computed from `X_train` alone.

### Constraints

- A column with zero standard deviation in the training data is scaled as if its standard deviation were `1`, so it becomes all zeros.
- Inputs are 2-D arrays with the same number of columns.
- Do not modify the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute `mean` and `std` from `X_train` only, with `axis=0`. Apply those same two arrays to both matrices.

</details>

<details>
<summary>Hint 2</summary>

Replace zero standard deviations with `1.0` using `np.where` before dividing.

</details>

## Theory

### The simple version

The scaler is a fitted object: it learns its numbers from the training data, then transforms anything else with those numbers. Re-fitting on the test data would quietly give the model a peek at the test set.

### The formula

$$
x' = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}, \qquad \sigma_{\text{train}} \leftarrow 1 \text{ wherever } \sigma_{\text{train}} = 0
$$

## Explanation

`standard_scale_no_leakage` computes the column means and standard deviations of the training matrix, replaces zero standard deviations with one, then applies the same two arrays to the training and test matrices. The test matrix is never used to compute any statistic.
