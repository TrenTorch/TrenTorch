---
name: math-expectation-variance-covariance
title: 'Expectation, Variance & Covariance'
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

**Summary statistics as operators**

`01-random-variables` already introduced `E[X]` as a weighted sum over a PMF. This question completes the trio of summary statistics that describe a distribution's _shape_, expectation (where its center of mass is), variance (how spread out it is), and covariance (how two variables move together), defined here as **operators on the population-level distribution itself**, not estimated from a finite sample. This distinction matters: the Bayesian Inference track's existing "expectation and variance from a sample" question computes an _estimator_ of these quantities from observed data; this question defines what that estimator is actually trying to estimate. Every loss function that's "the expected value of something" (expected reward in RL, expected negative log-likelihood in supervised learning) is built directly on this `E[\cdot]` operator.

**From a sample**

"What's the average test score" and "how spread out were the scores" are two different questions about the same list of numbers, and they're both estimates: you're using the students who actually took the test to guess something about "students in general," a quantity you can never observe directly. The average of your actual data is your best guess at the expectation; how far the data typically strays from that average is your best guess at the variance.

The subtlety worth catching early: there are two slightly different ways to compute "typical spread" from a sample, and using the wrong one for the wrong purpose silently biases every downstream calculation that depends on it, standard errors, confidence intervals, t-tests, all built later in this curriculum.

**Covariance & correlation**

Do people who spend more time studying tend to score higher on tests? Answering that isn't about either variable alone, `05-expectation-covariance`'s mean and variance describe study time and test scores separately, it's about whether they move together: when study time is above its own average, is score usually above its own average too? Covariance is the number that answers exactly that question, and correlation is the same idea, rescaled so its size doesn't depend on which units you happened to measure in (hours vs minutes, percent vs raw score).

This exact computation, "do these two variables move together," is what a covariance matrix full of, one entry per pair of features, and PCA (later, in Unsupervised Learning) literally finds its most informative directions by eigendecomposing exactly that matrix.

### From theory to code

**Summary statistics as operators**

Implement `expectation(values, probabilities)`, `variance(values, probabilities)`, and `pmf_covariance(x_values, y_values, joint_probabilities)`. The signatures and docstrings are already in the editor.

**From a sample**

Theory gives the mean as a direct average, and variance as average squared deviation from that mean, with one adjustable parameter (`ddof`) controlling which of the two standard divisors gets used.

Implement `sample_mean(x)` and `sample_variance(x, ddof=0)` against that reasoning. The signatures and docstrings are already in the editor.

**Covariance & correlation**

Theory defines covariance as the average product of each variable's deviation from its own mean, and correlation as covariance divided by both variables' standard deviations. Implement covariance first (reusing the same `ddof` convention `05-expectation-covariance` established), then correlation directly in terms of it.

Implement `covariance(x, y, ddof=0)` and `correlation(x, y)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

**Summary statistics as operators**

- `values`, `probabilities`, `x_values`, `y_values` are 1D array-likes; `probabilities` sums to 1.
- `joint_probabilities` is a 2D array-like where `joint_probabilities[i, j] = P(X=x_values[i], Y=y_values[j])`.
- Implement `variance` using `expectation` rather than duplicating its summation logic.

**From a sample**

- `x` is a 1D array of numeric samples.
- `sample_variance` must respect `ddof`: `ddof=0` divides by `n`, `ddof=1` divides by `n-1`.
- Both functions return a plain Python `float`.

**Covariance & correlation**

- `x` and `y` are 1D arrays of the same length.
- `covariance(x, x, ddof)` must equal `05-expectation-covariance`'s `sample_variance(x, ddof)`, they're the same formula with `y` set to `x`.
- `correlation`'s result must always fall in `[-1, 1]` (up to floating-point tolerance).

### Hints

**Summary statistics as operators**

<details>
<summary>Hint 1</summary>

`expectation` is the same weighted sum from `01-random-variables`: `np.sum(values * probabilities)`.

</details>

<details>
<summary>Hint 2</summary>

`variance` calls `expectation` to get the mean, then computes `np.sum(probabilities * (values - mean)**2)`, the probability-weighted average squared distance from that mean.

</details>

<details>
<summary>Hint 3</summary>

`pmf_covariance` needs each variable's own marginal first (`joint_probabilities.sum(axis=1)` for X, `axis=0` for Y, exactly as in `03-joint-independence`) to get `mean_x` and `mean_y`, then sums `joint_probabilities[i,j] * (x_i - mean_x) * (y_j - mean_y)` over every `(i, j)` pair.

</details>

**From a sample**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.mean` and `np.var` already exist and already accept a `ddof` argument, you are wrapping them, not deriving the formulas from a loop.

</details>

<details>
<summary>Hint 2</summary>

Don't hardcode `ddof=0` inside your implementation, pass the parameter straight through to `np.var`.

</details>

**Covariance & correlation**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Covariance is `mean((x - mean(x)) * (y - mean(y)))`, with the same `n` vs `n-ddof` divisor choice `05-expectation-covariance` uses.

</details>

<details>
<summary>Hint 2</summary>

`correlation` doesn't need its own formula from scratch, it's `covariance(x, y)` divided by `np.std(x) * np.std(y)`.

</details>

## Theory

### The simple version

**Summary statistics as operators**

`E[X]` is the distribution's center of mass, if you cut the PMF's bar chart out of cardboard, `E[X]` is exactly where it balances on a fingertip. `Var(X)` measures how far the mass is typically spread from that balance point, a distribution with all its mass right at the mean has variance 0; one with mass spread far in both directions has high variance. `Cov(X, Y)` measures whether two variables tend to be _simultaneously_ above or below their own means (positive covariance), simultaneously on opposite sides (negative covariance), or show no consistent pattern (covariance near 0, which is what independence forces, though the converse isn't always true).

**From a sample**

Ask ten random people their height and average the results: that average is your best guess at "the average height of everyone," even though you only measured ten people. Now ask "how much do heights vary": measure how far each of your ten people's heights sits from that average, square those distances (so a height 3 inches off counts the same whether it's 3 inches too tall or too short), and average the squared distances. That's variance, "typical squared distance from the average."

**Covariance & correlation**

Track two things about a group of students: hours studied and test score. If students who studied more consistently also scored higher, the two numbers "move together." Covariance measures this directly: for each student, multiply "how far above/below average was their study time" by "how far above/below average was their score." If both are consistently above average together (or both below together), those products are consistently positive, and the average of all those products is a large positive covariance. If one tends to be high when the other is low, the products are consistently negative.

### The formula

**Summary statistics as operators**

$$
E[X] = \sum_i x_i P(X=x_i), \qquad \text{Var}(X) = E\bigl[(X - E[X])^2\bigr] = \sum_i P(X=x_i)\,(x_i - E[X])^2
$$

$$
\text{Cov}(X, Y) = E\bigl[(X - E[X])(Y - E[Y])\bigr] = \sum_{i,j} P(X=x_i, Y=y_j)\,(x_i - E[X])(y_j - E[Y])
$$

- `E[\cdot]`, the expectation operator; it can be applied to any function of a random variable, not just `X` itself, `Var(X)` is literally `E[\cdot]` applied to the function `(X - E[X])^2`.
- `(x_i - E[X])`, the deviation of a specific outcome from the mean; squared in the variance formula so that deviations above and below the mean don't cancel out.
- `\sum_{i,j}`, a double sum over every combination of `X` and `Y`'s possible values, using the joint distribution's own probabilities.

**From a sample**

The **sample mean** estimates a distribution's expectation:

$$
\text{mean}(x) = \frac{1}{n}\sum_i x_i
$$

The **sample variance** estimates its variance, the average squared deviation from the mean:

$$
\text{variance}(x) = \frac{1}{D}\sum_i \left(x_i - \text{mean}(x)\right)^2
$$

where `D` is either `n` (dividing by the sample count directly, `ddof=0`) or `n - 1` (Bessel's correction, `ddof=1`). The `n-1` version exists because using the SAME sample to compute both the mean and the variance systematically underestimates the true variance, the sample mean is, by construction, the point closest to your own data, so deviations measured from it are slightly smaller than deviations from the true (unknown) population mean would be. Dividing by `n-1` instead of `n` exactly corrects that bias, on average. `np.var`'s default is `ddof=0` (a common source of quiet mismatches with `np.std(x, ddof=1)`-style code elsewhere), so `04-statistical-inference`'s confidence intervals and hypothesis tests, later in this curriculum, explicitly need to specify `ddof=1` for a statistically correct unbiased estimate.

**Covariance & correlation**

Covariance measures whether `x` and `y` tend to move together (positive), move oppositely (negative), or show no consistent relationship (near zero):

$$
\text{cov}(x, y) = \frac{1}{n - \text{ddof}}\sum_i \left(x_i - \text{mean}(x)\right)\left(y_i - \text{mean}(y)\right)
$$

Same `ddof` convention `05-expectation-covariance`'s `sample_variance` uses (in fact, `covariance(x, x, ddof)` is exactly `sample_variance(x, ddof)`, variance is just a variable's covariance with itself).

Covariance's magnitude depends on the variables' own scales (measuring study time in minutes instead of hours multiplies the covariance by 60, without the underlying relationship changing at all), which makes raw covariance hard to compare across different variable pairs. **Correlation** fixes this by dividing out each variable's own spread:

$$
\text{corr}(x, y) = \frac{\text{cov}(x, y)}{\text{std}(x) \cdot \text{std}(y)}
$$

This rescaling guarantees `corr(x, y)` always falls in `[-1, 1]`: `+1` means a perfect increasing linear relationship, `-1` a perfect decreasing one, `0` no linear relationship at all (note: no linear relationship, a variable can depend on another in a strong NON-linear way, like `y = x^2` and still show near-zero correlation).

### Why variance uses squared, not absolute, deviation

Using `|x_i - E[X]|` instead of `(x_i - E[X])^2` would also produce a non-negative "spread" measure (this is called mean absolute deviation, and is a valid statistic in its own right), but variance's squared form has properties absolute deviation lacks: it's differentiable everywhere (crucial for optimization, variance-based loss terms have smooth gradients, absolute-deviation-based ones don't at zero), and it decomposes cleanly under linear combinations of random variables (`Var(aX + bY) = a^2 Var(X) + b^2 Var(Y) + 2ab\,\text{Cov}(X,Y)`), which is why it, not mean absolute deviation, is the standard choice throughout probability and statistics.

### Try it live

**Summary statistics as operators**

<div class="tt-widget" data-widget="math-expectation-variance-covariance"></div>

**From a sample**

<div class="tt-widget" data-widget="math-expectation-variance"></div>

**Covariance & correlation**

<div class="tt-widget" data-widget="math-covariance-correlation"></div>

### How NumPy/PyTorch actually implements this

**Summary statistics as operators**

`np.average(values, weights=probabilities)` computes `expectation` directly (`np.mean` would be wrong here, it assumes equal weights, which is only correct when every outcome is equally likely). This question's population-level `variance`/`covariance`, defined directly from a known distribution, is the target that `np.var`/`np.cov` _estimate_ from finite samples when the true distribution isn't known, the Bayesian Inference track's sampling and estimation questions cover that sample-based estimation explicitly.

**From a sample**

`torch.var` mirrors this exact `ddof`/`correction` distinction (`correction=1` is PyTorch's modern default, matching the statistically unbiased convention, unlike NumPy's `ddof=0` default), and `torch.nn.BatchNorm1d`/`2d` internally computes a running mean and variance over each mini-batch using exactly these formulas, then uses them to normalize activations, one of the most common places "which variance convention" quietly matters in a real training loop: BatchNorm's running statistics (accumulated with `ddof=0`-style biased estimates, matching how the original paper defines it) and a manually-computed "unbiased" variance for reporting purposes are not interchangeable, and mixing them up produces subtly wrong normalization at inference time.

**Covariance & correlation**

`torch.cov` and `torch.corrcoef` compute exactly these formulas across every pair of rows in a 2D input at once, producing a full covariance/correlation matrix in one call, the object PCA (`06-unsupervised`) eigendecomposes to find a dataset's principal directions. Batch normalization (`torch.nn.BatchNorm2d`, seen throughout the Vision and Training tracks) implicitly relies on the _absence_ of strong correlation assumptions, it normalizes each feature channel independently using only its own mean and variance, deliberately ignoring cross-channel covariance for computational efficiency, a tradeoff that layer norm and group norm make differently.

## Explanation

**Summary statistics as operators.** `expectation` converts both inputs to float NumPy arrays and returns `np.sum(values * probabilities)`, the vectorized form of `Σ x_i P(x_i)`. `variance` calls `expectation` once to get `mean`, then returns `np.sum(probabilities * (values - mean) ** 2)`, reusing `expectation` rather than re-deriving the weighted-sum logic, exactly as the constraints require. `pmf_covariance` computes both marginals from the joint via `.sum(axis=1)`/`.sum(axis=0)` (mirroring `03-joint-independence`), gets `mean_x`/`mean_y` from `expectation`, then accumulates `joint_probabilities[i,j] * (x-mean_x) * (y-mean_y)` over every index pair with an explicit double loop, the direct, unoptimized translation of the double-sum formula, prioritizing clarity of correspondence to the math over vectorized performance.

**From a sample.** `sample_mean` wraps `np.mean(x)`, the direct average.

`sample_variance` wraps `np.var(x, ddof=ddof)`, passing the caller's `ddof` straight through rather than hardcoding either convention, so the same function serves both the biased and unbiased use cases from Theory.

**Covariance & correlation.** `covariance` computes both means, forms the elementwise product of deviations, sums it, and divides by `n - ddof`, exactly the formula from Theory (and identical to `sample_variance` when `y` is `x`).

`correlation` calls `covariance(x, y)` (with its default `ddof=0`, consistent since the divisor cancels between numerator and denominator regardless of which `ddof` is used, as long as it's the same throughout) and divides by `np.std(x) * np.std(y)`, the direct rescaling from Theory.
