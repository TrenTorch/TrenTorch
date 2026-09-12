---
name: math-covariance-correlation
title: Covariance and correlation between two variables
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Do people who spend more time studying tend to score higher on tests? Answering that isn't about either variable alone, `02-expectation-variance`'s mean and variance describe study time and test scores separately, it's about whether they move together: when study time is above its own average, is score usually above its own average too? Covariance is the number that answers exactly that question, and correlation is the same idea, rescaled so its size doesn't depend on which units you happened to measure in (hours vs minutes, percent vs raw score).

This exact computation, "do these two variables move together," is what a covariance matrix full of, one entry per pair of features, and PCA (later, in Unsupervised Learning) literally finds its most informative directions by eigendecomposing exactly that matrix.

### From theory to code

Theory defines covariance as the average product of each variable's deviation from its own mean, and correlation as covariance divided by both variables' standard deviations. Implement covariance first (reusing the same `ddof` convention `02-expectation-variance` established), then correlation directly in terms of it.

Implement `covariance(x, y, ddof=0)` and `correlation(x, y)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `x` and `y` are 1D arrays of the same length.
- `covariance(x, x, ddof)` must equal `02-expectation-variance`'s `sample_variance(x, ddof)`, they're the same formula with `y` set to `x`.
- `correlation`'s result must always fall in `[-1, 1]` (up to floating-point tolerance).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Covariance is `mean((x - mean(x)) * (y - mean(y)))`, with the same `n` vs `n-ddof` divisor choice `02-expectation-variance` uses.

</details>

<details>
<summary>Hint 2</summary>

`correlation` doesn't need its own formula from scratch, it's `covariance(x, y)` divided by `np.std(x) * np.std(y)`.

</details>

## Theory

### The simple version

Track two things about a group of students: hours studied and test score. If students who studied more consistently also scored higher, the two numbers "move together." Covariance measures this directly: for each student, multiply "how far above/below average was their study time" by "how far above/below average was their score." If both are consistently above average together (or both below together), those products are consistently positive, and the average of all those products is a large positive covariance. If one tends to be high when the other is low, the products are consistently negative.

### The formula

Covariance measures whether `x` and `y` tend to move together (positive), move oppositely (negative), or show no consistent relationship (near zero):

```text
cov(x, y) = (1/(n - ddof)) * sum((x_i - mean(x)) * (y_i - mean(y)))
```

Same `ddof` convention `02-expectation-variance`'s `sample_variance` uses (in fact, `covariance(x, x, ddof)` is exactly `sample_variance(x, ddof)`, variance is just a variable's covariance with itself).

Covariance's magnitude depends on the variables' own scales (measuring study time in minutes instead of hours multiplies the covariance by 60, without the underlying relationship changing at all), which makes raw covariance hard to compare across different variable pairs. **Correlation** fixes this by dividing out each variable's own spread:

```text
corr(x, y) = cov(x, y) / (std(x) * std(y))
```

This rescaling guarantees `corr(x, y)` always falls in `[-1, 1]`: `+1` means a perfect increasing linear relationship, `-1` a perfect decreasing one, `0` no linear relationship at all (note: no linear relationship, a variable can depend on another in a strong NON-linear way, like `y = x^2`, and still show near-zero correlation).

### How PyTorch actually implements this

`torch.cov` and `torch.corrcoef` compute exactly these formulas across every pair of rows in a 2D input at once, producing a full covariance/correlation matrix in one call, the object PCA (`06-unsupervised`) eigendecomposes to find a dataset's principal directions. Batch normalization (`torch.nn.BatchNorm2d`, seen throughout the Vision and Training tracks) implicitly relies on the _absence_ of strong correlation assumptions, it normalizes each feature channel independently using only its own mean and variance, deliberately ignoring cross-channel covariance for computational efficiency, a tradeoff that layer norm and group norm make differently.

## Explanation

`covariance` computes both means, forms the elementwise product of deviations, sums it, and divides by `n - ddof`, exactly the formula from Theory (and identical to `sample_variance` when `y` is `x`).

`correlation` calls `covariance(x, y)` (with its default `ddof=0`, consistent since the divisor cancels between numerator and denominator regardless of which `ddof` is used, as long as it's the same throughout) and divides by `np.std(x) * np.std(y)`, the direct rescaling from Theory.
