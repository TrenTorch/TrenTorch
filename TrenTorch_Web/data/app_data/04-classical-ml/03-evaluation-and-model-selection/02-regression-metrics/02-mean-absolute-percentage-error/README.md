---
name: evaluation-regression-mape
title: Mean absolute percentage error
tags: [classical-ml, evaluation, regression-metrics]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An error of 10 means something different for a house priced at 100 thousand than for one priced at 10 million. Mean absolute percentage error (MAPE) expresses each error as a fraction of the true value, then averages those fractions. The result reads as a percentage: a MAPE of 5 means the forecasts are off by about 5 percent on average.

Implement `mean_absolute_percentage_error(y_true, y_pred)`, which returns `100 * mean(|y_true - y_pred| / |y_true|)`.

### Constraints

- Shapes must match, otherwise raise `ValueError`.
- Any zero in `y_true` makes the percentage undefined: raise `ValueError`.
- Negative true values are allowed. The denominator uses their absolute value.
- Do not modify the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Divide the absolute error by the absolute true value elementwise, then take the mean, then multiply by 100.

</details>

<details>
<summary>Hint 2</summary>

Check `np.any(y_true == 0)` before dividing so the error message is clear.

</details>

## Theory

### The simple version

MAPE asks, on average, what fraction of the true value each forecast missed by. It is easy to read, but it punishes errors on small true values much harder than errors on large ones, and it cannot handle zeros at all.

### The formula

$$
\text{MAPE} = \frac{100}{n} \sum_{i=1}^{n} \frac{\lvert y_i - \hat{y}_i \rvert}{\lvert y_i \rvert}
$$

## Explanation

`mean_absolute_percentage_error` checks shapes and rejects zero targets, divides each absolute error by the absolute true value, averages, and scales to a percentage. Because the denominator is the true value, the same absolute error costs more when the true value is small. An over-forecast and an under-forecast of the same size score the same when they share a true value.
