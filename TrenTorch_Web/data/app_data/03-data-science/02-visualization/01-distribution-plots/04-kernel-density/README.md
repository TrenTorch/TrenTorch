---
name: data-science-kernel-density
title: Kernel Density Estimation
tags: [data-science, visualization, distributions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-histogram-bins` showed that a histogram's look depends on where its bins start and how wide they are, and its blocky bars are a poor picture of a smooth quantity. Kernel density estimation gives a smooth curve instead. Place a small bump, a kernel, on every data point and add them up: where data is dense the bumps pile up into a high ridge, and where it is sparse the curve is low. One number, the bandwidth, sets how wide each bump is, and it plays the role the bin width played, trading smoothness against detail. This question builds the estimator, a standard rule for choosing the bandwidth and a check that the result is a valid density.

### From theory to code

Implement `gaussian_kde(x, grid, bandwidth)`, which evaluates the density estimate at a set of points, then `silverman_bandwidth(x)`, a rule-of-thumb bandwidth, then `integrate_density(density, grid)`, which uses the trapezoid rule to check that the curve has total area one. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D float array of at least two values and `grid` is a 1D float array of the points at which to evaluate the density. `bandwidth` is a positive float.
- `gaussian_kde` returns an array the shape of `grid` where entry `j` is `mean_i( N(grid[j] - x[i]; 0, bandwidth) )`, the average of Gaussian bumps of standard deviation `bandwidth` centred on every data point. It raises `ValueError` if `bandwidth <= 0`.
- `silverman_bandwidth` returns `0.9 * min(std, IQR / 1.34) * n ** (-1/5)` as a float, where `std` is the sample standard deviation with `ddof=1`, `IQR` is the interquartile range from `np.percentile` and `n = len(x)`. If the minimum of the two spread measures is zero, it uses whichever is nonzero, and `1.0` if both are zero.
- `integrate_density(density, grid)` returns the trapezoid-rule area under the curve as a float, for a strictly increasing `grid`. Do not call `np.trapz` or `np.trapezoid`.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

A Gaussian bump of width `h` centred at `c` has height `exp(-0.5 * ((t - c) / h) ** 2) / (h * sqrt(2 * pi))` at `t`. Averaging one bump per data point keeps the total area at one.

</details>

<details>
<summary>Hint 2</summary>

Build an array of shape `(len(grid), len(x))` of differences with broadcasting, apply the bump formula and average over the data axis.

</details>

<details>
<summary>Hint 3</summary>

The trapezoid rule adds up, for every pair of neighbouring grid points, the gap between them times the average of the two heights.

</details>

## Theory

### The simple version

Drop a pebble in a pond at the position of every data point. Each pebble makes a small round ripple, and the water level at any spot is the sum of all the ripples there. Where many pebbles landed close together the water stands high, where few landed it stays low, and the whole surface is smooth. The bandwidth is how wide each ripple is: too narrow and you see one bump per pebble, too wide and everything melts into a single hump.

### The formula

Given data $x_1, \dots, x_n$ and a kernel $K$ (the standard normal density here), the **kernel density estimate** at $t$ with bandwidth $h$ is

$$
\hat{f}_h(t) = \frac{1}{n h}\sum_{i=1}^{n} K\!\left(\frac{t - x_i}{h}\right), \qquad K(u) = \frac{1}{\sqrt{2\pi}}\,e^{-u^2/2}
$$

Each term is a Gaussian bump of standard deviation $h$ centred on $x_i$, and averaging the $n$ bumps keeps the total area equal to $1$, so $\hat{f}_h$ is a valid density.

**Silverman's rule of thumb** picks the bandwidth from the data:

$$
h = 0.9\,\min\!\left(s,\ \frac{\mathrm{IQR}}{1.34}\right) n^{-1/5}
$$

where $s$ is the sample standard deviation. Using the smaller of the two spread measures keeps a few extreme values from over-smoothing the curve.

The **trapezoid rule** approximates the area under a curve sampled at points $t_0 < t_1 < \dots < t_m$ by

$$
\int \hat{f}\,dt \approx \sum_{j=0}^{m-1} \frac{\hat{f}(t_j) + \hat{f}(t_{j+1})}{2}\,(t_{j+1} - t_j)
$$

- A small $h$ gives a spiky curve that follows individual points (low bias, high variance). A large $h$ gives a smooth curve that can hide real structure (high bias, low variance).

### Bandwidth matters more than the kernel

The shape of the bump hardly changes the result. The width changes it a lot. Silverman's rule is tuned for roughly bell-shaped data and over-smooths a distribution with two well-separated peaks, so for multimodal data a smaller bandwidth, or a data-driven choice such as cross-validation, is used.

### Edges & bounded data

A Gaussian bump spills probability past the ends of the data. For a quantity that cannot be negative, such as a price, the curve leaks into negative values near zero. Common fixes are to estimate the density of the log of the data, or to reflect the bumps at the boundary.

### How NumPy/PyTorch actually implements this

`scipy.stats.gaussian_kde(x, bw_method='silverman')` is the standard implementation. `seaborn.kdeplot` and `pandas.Series.plot.kde` draw it, `sklearn.neighbors.KernelDensity` supports other kernels and cross-validated bandwidths, and `statsmodels.nonparametric.KDEUnivariate` adds fast FFT evaluation. Direct evaluation as done here costs `len(grid) * len(x)` operations, which is why large samples use binned or FFT versions.

## Explanation

`gaussian_kde` rejects a non-positive bandwidth, forms the matrix of scaled differences between every grid point and every data point by broadcasting, applies the Gaussian bump formula to it, and averages over the data axis, so every grid point receives the mean of the `n` bumps. `silverman_bandwidth` computes the sample standard deviation and the IQR scaled by 1.34, takes the smaller nonzero spread and applies the `0.9 * spread * n^(-1/5)` formula, falling back sensibly when the data has no spread. `integrate_density` multiplies each gap between neighbouring grid points by the mean of the two heights at its ends and sums them, which is the trapezoid rule written out directly.
