---
name: data-science-quantile-plots
title: 'Quantile-Quantile Plots'
tags: [data-science, visualization, distributions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Whether a column is normally distributed decides which statistical tests are fair, whether a linear model's errors are well behaved and whether a log transform from `04-skew-transforms` worked. A histogram lets the eye judge bell-shapedness badly. A quantile-quantile plot makes the question a straight-line check: sort the data, pair each sorted value with the value a perfect normal sample would have in the same position, and plot one against the other. If the data is normal the points fall on a line, and the way they bend away from it says exactly how the distribution differs: heavy tails, skew, a flat top. This question builds the numbers behind that plot, including the inverse of the normal CDF that supplies the reference values.

### From theory to code

Implement `normal_ppf(p)`, the value below which a standard normal falls with probability `p`, then `plotting_positions(n)`, the probabilities assigned to the `n` sorted values, then `qq_points(x)`, the two coordinate arrays of the plot, then `qq_line(theoretical, sample)`, the reference line through the quartiles, then `qq_correlation(x)`, one number that summarizes how straight the plot is. The signatures and docstrings are already in the editor.

### Constraints

- `normal_ppf(p)` returns the standard normal quantile of `p` as a float, accurate to at least `1e-9`, for `0 < p < 1`. It raises `ValueError` for any other `p`. Do not use `scipy`. Use `math.erf` and bisection (or another method you write).
- `plotting_positions(n)` returns the array `(i - 0.5) / n` for `i = 1 .. n`.
- `qq_points(x)` returns `(theoretical, sample)`: `sample` is `x` sorted ascending and `theoretical[i] = normal_ppf(plotting_positions(n)[i])`, both 1D float arrays of length `n`.
- `qq_line(theoretical, sample)` returns `(slope, intercept)` of the line through the points at the 25th and 75th percentiles of the two arrays (`np.percentile`, linear interpolation): `slope = (s75 - s25) / (t75 - t25)` and `intercept = s25 - slope * t25`.
- `qq_correlation(x)` returns the Pearson correlation between `theoretical` and `sample` from `qq_points(x)`, as a float.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

The normal CDF is `0.5 * (1 + erf(z / sqrt(2)))` and is strictly increasing, so its inverse can be found by narrowing an interval around the answer, halving it each time.

</details>

<details>
<summary>Hint 2</summary>

The `- 0.5` in the plotting positions keeps the probabilities strictly inside `(0, 1)`, so no sorted value is paired with an infinite quantile.

</details>

<details>
<summary>Hint 3</summary>

If the data is exactly `mean + std * z` for normal `z`, the sample quantiles are a straight function of the theoretical ones, with slope equal to the standard deviation and intercept equal to the mean.

</details>

## Theory

### The simple version

Suppose you lined up a hundred perfectly normal people by height. The shortest would be about 2.5 standard deviations below average, the middle one at the average and the tallest 2.5 above. A Q-Q plot lines up your real data the same way and compares each person with that ideal. If your data really is normal, each person lands where the ideal says and the points form a straight diagonal. If the tallest people are much taller than the ideal predicts, the right end of the plot curls upward and tells you the tail is too heavy.

### The formula

Sort the data $x_{(1)} \le \dots \le x_{(n)}$ and give the $i$-th value the probability

$$
p_i = \frac{i - 0.5}{n}
$$

The **theoretical quantile** of the standard normal at $p_i$ is $z_i = \Phi^{-1}(p_i)$, where $\Phi$ is the normal CDF

$$
\Phi(z) = \tfrac{1}{2}\left(1 + \operatorname{erf}\!\left(\frac{z}{\sqrt{2}}\right)\right)
$$

A **Q-Q plot** plots the points $(z_i,\ x_{(i)})$. If $x \sim \mathcal{N}(\mu, \sigma^2)$ then $x_{(i)} \approx \mu + \sigma z_i$, so the points lie near a line with slope $\sigma$ and intercept $\mu$.

- A **reference line** through the first and third quartile points, rather than a least-squares fit, is robust to tails: it describes the middle of the data and lets the tails show how they differ.
- The **probability plot correlation** $r = \operatorname{corr}(z, x_{(i)})$ is close to $1$ for normal data. Lower values signal curvature.

Reading the shape: an S-shape with the ends curling away from the line means heavier tails than normal, a curve that bends one way throughout means skew, and a plot that is steeper in the middle than the line means lighter tails.

### Any reference distribution

Replacing the normal quantiles with the quantiles of another distribution (exponential, t, uniform) tests fit to that distribution. Plotting the sorted values of one sample against the sorted values of another, with no theoretical reference, compares two samples directly, which is how a training and a validation distribution are compared.

### Small samples

With fewer than about 30 points, even truly normal data wanders visibly off the line. A Q-Q plot is a picture to look at, not a test with a pass mark, and a statistical test such as Shapiro-Wilk or Anderson-Darling gives a number to go with it.

### How NumPy/PyTorch actually implements this

`scipy.stats.norm.ppf(p)` is the inverse normal CDF, and `scipy.stats.probplot(x, dist='norm')` returns exactly the points and the line fitted here (with a least-squares fit by default). `statsmodels.api.qqplot` and `scipy.stats.probplot(..., plot=plt)` draw it. `torch.distributions.Normal(0, 1).icdf(p)` is the PyTorch inverse CDF, and `torch.erfinv` gives it through `sqrt(2) * erfinv(2p - 1)`.

## Explanation

`normal_ppf` rejects probabilities outside the open interval and then bisects: it starts with a wide bracket around zero, evaluates the normal CDF built from `math.erf` at the midpoint and halves the bracket toward the side that contains `p`, repeating until the interval is far narrower than the required accuracy. `plotting_positions` is `(arange(1, n + 1) - 0.5) / n`. `qq_points` sorts the data and applies `normal_ppf` to each plotting position, so the two returned arrays line up index by index. `qq_line` takes the quartiles of both arrays and computes the slope between the two quartile points and the intercept that makes the line pass through the lower one. `qq_correlation` is the Pearson correlation of the two arrays from `qq_points`, which is near one for normal data and falls as the plot curves.
