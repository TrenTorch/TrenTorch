---
name: evaluation-regression-explained-variance
title: Explained variance score
tags: [classical-ml, evaluation, regression-metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`R-squared score` penalizes a prediction that is shifted away from the truth, because the shift shows up in the residual sum of squares. Sometimes that is not what you want. If a model is consistently 3 units too high but otherwise tracks every movement of the target perfectly, the explained variance score ignores the constant offset and still rewards the model for tracking the variation. It measures how much of the target's variance the errors fail to explain, with the mean error removed.

Implement `explained_variance_score(y_true, y_pred)`, which returns `1 - Var(y_true - y_pred) / Var(y_true)`, using population variance (`ddof = 0`).

### Constraints

- Shapes must match, otherwise raise `ValueError`.
- If `y_true` is constant, `Var(y_true)` is zero: raise `ValueError`.
- A constant offset in the predictions leaves the score at `1`.
- Do not modify the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.var` already subtracts the mean, so `np.var(y_true - y_pred)` ignores a constant offset automatically.

</details>

<details>
<summary>Hint 2</summary>

Check `np.var(y_true) == 0` before dividing, the same way the R-squared question checks for a constant target.

</details>

## Theory

### The simple version

Variance measures how spread out values are around their own mean. The score asks what fraction of the target's spread the prediction reproduces. Subtracting a constant from the prediction does not change the spread of the errors, so the score does not change either.

### The formula

$$
\text{EVS} = 1 - \frac{\operatorname{Var}(y - \hat{y})}{\operatorname{Var}(y)}
$$

## Explanation

`explained_variance_score` checks shapes and constancy, then computes the population variance of the residuals and divides by the population variance of the target. Because `np.var` centers each array first, the function reproduces the offset invariance described in Theory.
