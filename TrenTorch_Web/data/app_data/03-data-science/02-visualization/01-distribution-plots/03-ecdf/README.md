---
name: data-science-ecdf
title: Empirical CDF
tags: [data-science, visualization, distributions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A histogram needs a bin width and a box plot throws away shape. The empirical cumulative distribution function, ECDF, needs no tuning at all: for every value on the horizontal axis it shows the fraction of the data at or below that value. It uses every data point, it makes quartiles and percentiles readable straight off the curve, and putting two ECDFs on one plot shows at once whether one sample sits above, below or crosses the other. The largest vertical gap between two ECDFs is itself a statistic, the Kolmogorov-Smirnov distance, which is how a model's score distributions or a feature before and after a shift get compared. This question builds the curve, evaluates it anywhere and measures that gap.

### From theory to code

Implement `ecdf(x)`, the points of the staircase, then `ecdf_at(x, points)`, the curve's height at arbitrary places, then `ks_distance(x, y)`, the largest vertical gap between the ECDFs of two samples. The signatures and docstrings are already in the editor.

### Constraints

- `x` and `y` are 1D float arrays with at least one value.
- `ecdf(x)` returns `(values, probabilities)`: `values` is `x` sorted ascending and `probabilities[i] = (i + 1) / n`, so the last probability is `1.0`. Repeated values each get their own entry.
- `ecdf_at(x, points)` returns a float array with the fraction of entries of `x` that are less than or equal to each point. It works for any array of query points and does not require them to be in `x`.
- `ks_distance(x, y)` returns `max over all t of |F_x(t) - F_y(t)|` as a float, where `F` is the ECDF of each sample. The maximum only needs to be checked at the values that occur in either sample.
- Do not call `scipy`. Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

`np.searchsorted(sorted_x, points, side="right")` counts how many sorted values are less than or equal to each point, which divided by `n` is the ECDF.

</details>

<details>
<summary>Hint 2</summary>

Between two data points the ECDF is flat, and it only jumps at data values. The largest gap between two such step functions therefore happens at one of those jump locations.

</details>

<details>
<summary>Hint 3</summary>

Evaluate both ECDFs at the pooled values from both samples and take the largest absolute difference.

</details>

## Theory

### The simple version

Ask a hundred people their height and line them up from shortest to tallest. The ECDF answers "what share of the room is this tall or shorter?" for any height: it is zero below the shortest person, climbs one hundredth at each person and reaches one at the tallest. Draw two rooms' curves on the same axes and the room whose curve sits further to the right is the taller one, with no choice of bin widths involved.

### The formula

For a sample $x_1, \dots, x_n$ the **empirical CDF** is

$$
\hat{F}(t) = \frac{1}{n}\sum_{i=1}^{n} \mathbf{1}\{x_i \le t\}
$$

the fraction of the sample at or below $t$. It is a staircase that is $0$ below the smallest value, rises by $1/n$ at each data point and is $1$ from the largest value on. With the data sorted as $x_{(1)} \le \dots \le x_{(n)}$, the plotted points are $\big(x_{(i)},\ i/n\big)$.

The **Kolmogorov-Smirnov distance** between two samples is the largest vertical gap between their ECDFs:

$$
D = \sup_{t}\ \big|\hat{F}_x(t) - \hat{F}_y(t)\big|
$$

- $D = 0$ means the two samples have identical distributions in the data, and $D = 1$ means they do not overlap at all.
- Because both curves are flat between data values, the supremum is reached at one of the pooled sample values.
- The ECDF converges to the true CDF as $n$ grows, and its uniform error shrinks at rate about $1/\sqrt{n}$ (the Dvoretzky-Kiefer-Wolfowitz inequality).

### Reading percentiles off the curve

The value where the ECDF first reaches 0.5 is the median, and where it reaches 0.9 is the 90th percentile. A steep part of the curve is a region where many data points sit close together, and a flat part is a gap. That makes the ECDF a histogram that never needs a bin width.

### Two-sample comparisons

The KS distance is the test statistic of the two-sample Kolmogorov-Smirnov test for "do these two samples come from the same distribution?". In machine learning it is a quick drift check between training and live feature values, and the largest gap between the score ECDFs of positive and negative examples is the KS statistic reported for credit-scoring models.

### How NumPy/PyTorch actually implements this

`statsmodels.distributions.empirical_distribution.ECDF(x)` returns a callable ECDF, and `scipy.stats.ecdf` is the SciPy equivalent. `scipy.stats.ks_2samp(x, y)` computes the KS distance with a p-value. `seaborn.ecdfplot` and `matplotlib` step plots draw it. `np.searchsorted` on a sorted array is the standard way to evaluate it at many points at once.

## Explanation

`ecdf` sorts the sample and pairs each sorted value with `(i + 1) / n`, so the probabilities rise by one over `n` per entry and finish at one. `ecdf_at` sorts a copy of the sample, uses `np.searchsorted(side="right")` to count how many entries are less than or equal to each query point, and divides by `n`. `ks_distance` pools the values of both samples, evaluates the two ECDFs at every pooled value with `ecdf_at`, and returns the largest absolute difference, which is the supremum because the curves are flat between those points.
