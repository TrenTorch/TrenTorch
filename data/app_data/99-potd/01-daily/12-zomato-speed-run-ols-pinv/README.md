---
name: potd-zomato-speed-run-ols-pinv
title: 'ZOMATO SPEED-RUN'
tags: [classical-ml, linear-algebra]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Classic ML, Linear Algebra

---

### Story

In Zomato's early growth phase, the delivery-time feature had zero pipeline maturity: no
gradient-boosted trees, no feature store, just a spreadsheet of past deliveries. The team needs a
linear estimator working today. You are given distance and historical delivery time for `n` past
orders; fit ordinary least squares via the closed-form normal equation and predict on new orders.

---

### The Math

With the intercept folded into `X` as a leading column of ones:

```
w = (X^T X)^-1 X^T y
```

Because production data occasionally has duplicated or near-collinear feature columns, a literal
inverse can fail. Use the Moore-Penrose pseudo-inverse (SVD-based) instead of a hard inverse.

### Input Format

```
n d
x_1,1 ... x_1,d y_1
...
x_n,1 ... x_n,d y_n
m
q_1,1 ... q_1,d
...
q_m,1 ... q_m,d
```

### Output Format

First line: fitted coefficients (intercept, then `w_1..w_d`) to 6 decimals. Next `m` lines:
predicted values to 6 decimals.

### Constraints

- `1 <= n <= 10^4`, `1 <= d <= 20`, `1 <= m <= 10^3`
- Time limit: 2.0 seconds. Memory: 256 MB.

---

### Example

**Input**

```
3 1
1 5
2 7
3 9
2
4
5
```

**Output**

```
3.000000 2.000000
11.000000
13.000000
```

**Explanation:** The data is exactly `y = 2x + 3`, so the fit recovers it exactly: intercept `3.0`,
slope `2.0`. Predictions at `x = 4, 5` are `11` and `13`.

## Theory

### The simple version

Least squares finds the line (or plane) that stays closest, on average, to every point in your data. The pseudo-inverse is a more forgiving way to solve for that line when some of your features are redundant or nearly duplicates of each other.

### Why the pseudo-inverse, not `inv`

`X^T X` can be singular: two feature columns that are exact multiples of each other, or `n <= d`,
both make it non-invertible. A literal `inv()` call throws or returns garbage on a singular matrix.
`pinv` (built on the SVD) always returns an answer, and for a singular system it returns the
minimum-norm solution among the infinitely many weight vectors that fit the data equally well.

### Predictions are well-defined even when weights are not

When `X^T X` is singular there are infinitely many weight vectors that produce identical
predictions on the training data. The predictions themselves are still the right thing to check for
correctness; the raw weight vector is not, unless the system is well-conditioned.

### Feature scale

Distance in meters next to a 0/1 flag is a wide difference in scale. The pseudo-inverse handles this
correctly because the SVD it is built on is scale-aware; a naive elimination-based solver is more
exposed to conditioning problems at wide scale differences.

## Explanation

`ols_fit_predict` prepends a column of ones to `X` (so the intercept is just another weight),
computes `w = np.linalg.pinv(X_aug) @ y`, and predicts with `Q_aug @ w` after prepending the same
column of ones to the query matrix. Using `pinv` instead of `inv(X.T @ X) @ X.T` means a
perfectly collinear or underdetermined system never crashes: the SVD inside `pinv` degrades
gracefully to the minimum-norm solution instead of dividing by a zero singular value.
