---
name: numpy-descriptive-statistics
title: Descriptive Statistics
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement the summary statistics an analyst reaches for first, from their definitions. `percentiles` returns chosen percentiles of a sample (linear interpolation), `iqr` the interquartile range, `zscores` standardises a sample to mean 0 and standard deviation 1, `pearson` is the Pearson correlation of two samples computed from its formula (without calling `np.corrcoef`), and `covariance_matrix` is the sample covariance matrix of the columns of a 2D array (without calling `np.cov`).

## Theory

### Percentiles

The $q$-th percentile is the value below which $q\%$ of the data lies. With linear interpolation, NumPy places the data at positions $0, 1, \dots, n-1$ of the sorted array and reads position $\frac{q}{100}(n-1)$, interpolating between neighbours when that is not a whole number:

```python
np.percentile([1, 2, 3, 4], 50)         # 2.5   position 1.5 -> between 2 and 3
np.percentile([1, 2, 3, 4], [25, 75])   # [1.75, 3.25]
```

The **interquartile range** $\text{IQR} = Q_3 - Q_1$ measures spread and ignores the extremes.

### Standardising

$$
z_i = \frac{x_i - \bar{x}}{\sigma}, \qquad \sigma = \sqrt{\frac{1}{n}\sum_i (x_i-\bar{x})^2}
$$

The result has mean 0 and standard deviation 1, which puts different variables on one scale. If $\sigma = 0$ every value equals the mean, and the sensible answer is all zeros rather than a division by zero.

### Correlation and covariance

For samples $x$ and $y$ of length $n$,

$$
r = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i (x_i-\bar{x})^2}\ \sqrt{\sum_i (y_i-\bar{y})^2}}
$$

For the columns of a data matrix $X$ ($n$ rows, $d$ columns), with $X_c$ the matrix after subtracting each column's mean, the **sample covariance matrix** is

$$
\Sigma = \frac{1}{n-1} X_c^{\top} X_c
$$

Entry $(j, k)$ is the covariance of columns $j$ and $k$; the diagonal holds the variances (with $n-1$, the _sample_ variance).

### ddof

`np.std` and `np.var` divide by $n$ by default (`ddof=0`, the population version). `ddof=1` divides by $n-1$. Covariance estimators conventionally use $n-1$, standardisation here uses $n$.

### How NumPy implements this

`np.percentile` sorts a copy (or partitions it) and interpolates. The covariance is one matrix product $X_c^{\top}X_c$, a single BLAS call, which is why computing it with matrix multiplication is far faster than looping over pairs of columns.

## Explanation

`percentiles` calls `np.percentile` with linear interpolation. `iqr` is the difference between the 75th and 25th percentiles. `zscores` subtracts the mean and divides by the population standard deviation, returning zeros when that is zero. `pearson` centres both samples, then divides the sum of products by the product of the root sums of squares. `covariance_matrix` centres each column and computes `Xc.T @ Xc / (n - 1)`.
