---
name: evaluation-regression-r2-score
title: R-squared score
tags: [classical-ml, evaluation, regression-metrics]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Mean squared error tells you how large the errors are, but not whether they are large relative to the spread of the target. A regressor that misses by 5 units is excellent when the target ranges over 1000 and poor when it ranges over 6. The R-squared score fixes that by comparing the model's squared error against the error of the simplest possible model, one that always predicts the mean of the target.

Implement `r2_score(y_true, y_pred)`, which returns `1 - SS_res / SS_tot`.

### Constraints

- `y_true` and `y_pred` must have the same shape, otherwise raise `ValueError`.
- If `y_true` is constant, `SS_tot` is zero and the score is undefined: raise `ValueError`.
- A perfect prediction scores `1`. Predicting the mean scores `0`. Worse predictions score below `0`.
- Do not modify the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`SS_tot` is the sum of squared differences from the mean of `y_true`. `SS_res` is the sum of squared differences between `y_true` and `y_pred`.

</details>

<details>
<summary>Hint 2</summary>

Check for a constant target with `np.all(y_true == y_true[0])` before dividing, so the error is raised for real and not from a division warning.

</details>

## Theory

### The simple version

Take the mean-predicting model as the baseline. R-squared measures what fraction of the baseline's squared error your model removed. A score of `0.8` means the model removes 80 percent of the squared error that the mean would have left behind.

### The formula

$$
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}
$$

## Explanation

`r2_score` converts both inputs to float arrays, checks shapes and constancy, then returns one minus the ratio of the residual sum of squares to the total sum of squares. The constancy check is what keeps the denominator from being zero.
