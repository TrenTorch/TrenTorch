---
name: math-expectation-variance-covariance
title: 'Expectation, Variance and Covariance as Operators'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-random-variables` already introduced `E[X]` as a weighted sum over a PMF. This question completes the trio of summary statistics that describe a distribution's _shape_ — expectation (where its center of mass is), variance (how spread out it is), and covariance (how two variables move together) — defined here as **operators on the population-level distribution itself**, not estimated from a finite sample. This distinction matters: the Bayesian Inference track's existing "expectation and variance from a sample" question computes an _estimator_ of these quantities from observed data; this question defines what that estimator is actually trying to estimate. Every loss function that's "the expected value of something" (expected reward in RL, expected negative log-likelihood in supervised learning) is built directly on this `E[\cdot]` operator.

### From theory to code

Implement `expectation(values, probabilities)`, `variance(values, probabilities)`, and `covariance(x_values, y_values, joint_probabilities)`. The signatures and docstrings are already in the editor.

### Constraints

- `values`, `probabilities`, `x_values`, `y_values` are 1D array-likes; `probabilities` sums to 1.
- `joint_probabilities` is a 2D array-like where `joint_probabilities[i, j] = P(X=x_values[i], Y=y_values[j])`.
- Implement `variance` using `expectation` rather than duplicating its summation logic.

### Hints

<details>
<summary>Hint 1</summary>

`expectation` is the same weighted sum from `01-random-variables`: `np.sum(values * probabilities)`.

</details>

<details>
<summary>Hint 2</summary>

`variance` calls `expectation` to get the mean, then computes `np.sum(probabilities * (values - mean)**2)` — the probability-weighted average squared distance from that mean.

</details>

<details>
<summary>Hint 3</summary>

`covariance` needs each variable's own marginal first (`joint_probabilities.sum(axis=1)` for X, `axis=0` for Y, exactly as in `04-joint-and-marginal-probability`) to get `mean_x` and `mean_y`, then sums `joint_probabilities[i,j] * (x_i - mean_x) * (y_j - mean_y)` over every `(i, j)` pair.

</details>

## Theory

### The simple version

`E[X]` is the distribution's center of mass — if you cut the PMF's bar chart out of cardboard, `E[X]` is exactly where it balances on a fingertip. `Var(X)` measures how far the mass is typically spread from that balance point — a distribution with all its mass right at the mean has variance 0; one with mass spread far in both directions has high variance. `Cov(X, Y)` measures whether two variables tend to be _simultaneously_ above or below their own means (positive covariance), simultaneously on opposite sides (negative covariance), or show no consistent pattern (covariance near 0, which is what independence forces, though the converse isn't always true).

### The formula

$$
E[X] = \sum_i x_i P(X=x_i), \qquad \text{Var}(X) = E\bigl[(X - E[X])^2\bigr] = \sum_i P(X=x_i)\,(x_i - E[X])^2
$$

$$
\text{Cov}(X, Y) = E\bigl[(X - E[X])(Y - E[Y])\bigr] = \sum_{i,j} P(X=x_i, Y=y_j)\,(x_i - E[X])(y_j - E[Y])
$$

- `E[\cdot]` — the expectation operator; it can be applied to any function of a random variable, not just `X` itself — `Var(X)` is literally `E[\cdot]` applied to the function `(X - E[X])^2`.
- `(x_i - E[X])` — the deviation of a specific outcome from the mean; squared in the variance formula so that deviations above and below the mean don't cancel out.
- `\sum_{i,j}` — a double sum over every combination of `X` and `Y`'s possible values, using the joint distribution's own probabilities.

### Why variance uses squared, not absolute, deviation

Using `|x_i - E[X]|` instead of `(x_i - E[X])^2` would also produce a non-negative "spread" measure (this is called mean absolute deviation, and is a valid statistic in its own right) — but variance's squared form has properties absolute deviation lacks: it's differentiable everywhere (crucial for optimization — variance-based loss terms have smooth gradients, absolute-deviation-based ones don't at zero), and it decomposes cleanly under linear combinations of random variables (`Var(aX + bY) = a^2 Var(X) + b^2 Var(Y) + 2ab\,\text{Cov}(X,Y)`), which is why it — not mean absolute deviation — is the standard choice throughout probability and statistics.

### How NumPy/PyTorch actually implements this

`np.average(values, weights=probabilities)` computes `expectation` directly (`np.mean` would be wrong here — it assumes equal weights, which is only correct when every outcome is equally likely). This question's population-level `variance`/`covariance`, defined directly from a known distribution, is the target that `np.var`/`np.cov` _estimate_ from finite samples when the true distribution isn't known — the Bayesian Inference track's sampling and estimation questions cover that sample-based estimation explicitly.

## Explanation

`expectation` converts both inputs to float NumPy arrays and returns `np.sum(values * probabilities)`, the vectorized form of `Σ x_i P(x_i)`. `variance` calls `expectation` once to get `mean`, then returns `np.sum(probabilities * (values - mean) ** 2)` — reusing `expectation` rather than re-deriving the weighted-sum logic, exactly as the constraints require. `covariance` computes both marginals from the joint via `.sum(axis=1)`/`.sum(axis=0)` (mirroring `04-joint-and-marginal-probability`), gets `mean_x`/`mean_y` from `expectation`, then accumulates `joint_probabilities[i,j] * (x-mean_x) * (y-mean_y)` over every index pair with an explicit double loop — the direct, unoptimized translation of the double-sum formula, prioritizing clarity of correspondence to the math over vectorized performance.
