---
name: data-science-monte-carlo-estimation
title: Monte Carlo Estimation
tags: [data-science, simulation, probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Many quantities worth knowing have no tidy formula: the expected profit of a pricing rule, the chance a project finishes late, the area of an awkward shape. Monte Carlo estimation replaces the formula with an experiment. Draw many random samples, compute what you care about on each one, and average. The law of large numbers says the average closes in on the true value, and a second fact, how fast the error shrinks, tells you how many samples you need. This question builds the estimator, two classic uses of it and the sample-size rule.

### From theory to code

Implement `monte_carlo_mean(f, sampler, n, rng)`, which estimates an expectation and its error, then `estimate_pi(n, rng)`, which estimates pi by throwing random points at a square, then `monte_carlo_integral(f, a, b, n, rng)`, which estimates a definite integral, then `samples_for_precision(std, target_se)`, which says how many samples reach a target error. The signatures and docstrings are already in the editor.

### Constraints

- `sampler(rng, n)` returns a 1D float array of `n` independent draws from the distribution of interest. `f` takes that array and returns an array of the same length, one value per draw.
- `monte_carlo_mean` calls `sampler(rng, n)` exactly once and returns `(estimate, standard_error)` as floats, where `estimate` is the mean of `f(samples)` and `standard_error` is its sample standard deviation (with `ddof=1`) divided by `sqrt(n)`. It requires `n >= 2`.
- `estimate_pi` draws `x = rng.random(n)` first and then `y = rng.random(n)`, counts the points with `x**2 + y**2 <= 1` and returns `4 * count / n` as a float.
- `monte_carlo_integral` draws `u = rng.uniform(a, b, size=n)` once and returns `(b - a) * mean(f(u))` as a float, where `f` is vectorized.
- `samples_for_precision` returns the smallest integer `n` with `std / sqrt(n) <= target_se`, that is `ceil((std / target_se) ** 2)`, as an int. It raises `ValueError` if `target_se <= 0`.

### Hints

<details>
<summary>Hint 1</summary>

An expectation is an average over the distribution, so an average over many draws from it estimates it. The standard error is the standard deviation of that average, which shrinks as the number of draws grows.

</details>

<details>
<summary>Hint 2</summary>

For pi, the quarter circle of radius 1 inside the unit square has area pi/4, so the fraction of random points that land inside it estimates pi/4.

</details>

<details>
<summary>Hint 3</summary>

To integrate, remember that the integral of f over an interval is the interval's length times the average value of f on it.

</details>

## Theory

### The simple version

To find the average height of everyone in a city you could measure all of them, or you could measure a few thousand picked at random and average. The second is a Monte Carlo estimate. It is never exactly right, but it is close, and you can say _how_ close: the more people you measure, the smaller the typical miss, shrinking in proportion to one over the square root of the number measured.

### The formula

To estimate $\mu = \mathbb{E}[f(X)]$, draw $X_1, \dots, X_n$ independently from the distribution of $X$ and average:

$$
\hat{\mu}_n = \frac{1}{n}\sum_{i=1}^{n} f(X_i)
$$

The estimate is unbiased, and its typical error, the **standard error**, is

$$
\operatorname{SE}(\hat{\mu}_n) = \frac{\sigma}{\sqrt{n}}, \qquad \hat{\sigma}^2 = \frac{1}{n-1}\sum_{i}\big(f(X_i) - \hat{\mu}_n\big)^2
$$

- Halving the error costs four times as many samples, because the error falls as $1/\sqrt{n}$. This rate does not depend on how many dimensions the problem has, which is why Monte Carlo is the tool of choice for high-dimensional integrals.
- To reach a target standard error $\varepsilon$ you need $n \ge (\sigma/\varepsilon)^2$ samples.

**Estimating pi.** With $(x, y)$ uniform on the unit square, $P(x^2 + y^2 \le 1) = \pi/4$, so $\pi \approx 4 \times (\text{fraction inside the circle})$.

**Integrals.** For an interval $[a, b]$,

$$
\int_a^b f(x)\,dx = (b - a)\,\mathbb{E}\big[f(U)\big], \qquad U \sim \text{Uniform}(a, b)
$$

### Reproducibility

A simulation that cannot be repeated cannot be debugged. Passing an explicit random generator into every function, and seeding it once at the top, makes a run repeatable and lets two runs be compared on the same random numbers.

### Where the plain version struggles

When the event of interest is rare, almost every draw contributes zero and the estimate is dominated by luck. The next question, `02-importance-sampling`, reshapes where the draws come from to fix exactly that.

### How NumPy/PyTorch actually implements this

`rng.random(n)`, `rng.normal(size=n)` and `rng.uniform(a, b, size=n)` produce the draws, and `np.mean` and `np.std(ddof=1)` give the estimate and the spread. `scipy.integrate.quad` integrates one-dimensional functions deterministically and is far more accurate there, while `scipy.stats.qmc` supplies low-discrepancy sequences that converge faster than plain Monte Carlo. In PyTorch, `torch.randn` and `torch.rand` are the same draws on tensors, and Monte Carlo averaging over sampled noise is how stochastic objectives such as the variational lower bound are estimated.

## Explanation

`monte_carlo_mean` asks the sampler for all `n` draws in one call, applies `f` to the whole array, and returns the mean and the sample standard deviation with `ddof=1` divided by `sqrt(n)`, the standard error formula from Theory. `estimate_pi` draws the `x` coordinates and then the `y` coordinates in that fixed order, counts the points inside the unit circle and scales the fraction by four. `monte_carlo_integral` draws `n` uniform points on `[a, b]`, averages `f` over them and multiplies by the interval length. `samples_for_precision` rearranges `std / sqrt(n) <= target_se` into `n >= (std / target_se)^2` and rounds up with `ceil` so the guarantee holds.
