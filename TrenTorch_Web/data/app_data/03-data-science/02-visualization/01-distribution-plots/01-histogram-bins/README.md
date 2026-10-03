---
name: data-science-histogram-bins
title: Histogram Bins
tags: [data-science, visualization, distributions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A histogram is the first plot anyone draws of a numeric column, and everything it shows depends on a choice made before any ink is spent: how wide the bins are. Too few bins and a two-humped distribution looks like one hump. Too many and the picture is a comb of single-row spikes that shows noise instead of shape. A chart is a drawing of numbers, so what can be tested is the numbers behind it: the bin edges and the count in each bin. This question builds both, and two standard rules for choosing how many bins there should be.

### From theory to code

Implement `sturges_bins(n)`, the bin count from Sturges' rule, then `freedman_diaconis_bins(x)`, the bin count from the Freedman-Diaconis rule, then `bin_edges(x, n_bins)`, the equal-width edges spanning the data, then `histogram_counts(x, edges)`, how many values fall in each bin. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D float array with at least two values and at least two distinct values. `n` is the number of values.
- `sturges_bins(n)` returns `ceil(log2(n)) + 1` as an int, for `n >= 1`.
- `freedman_diaconis_bins(x)` uses bin width `2 * IQR / n ** (1/3)`, where `IQR` is the difference between the 75th and 25th percentiles (linear interpolation, as `np.percentile` does by default). It returns `ceil((max - min) / width)` as an int, and at least `1`. If the IQR is zero it falls back to `sturges_bins(len(x))`.
- `bin_edges(x, n_bins)` returns `n_bins + 1` equally spaced edges from `min(x)` to `max(x)` inclusive.
- `histogram_counts(x, edges)` returns an integer array of length `len(edges) - 1`. A value `v` belongs to bin `i` when `edges[i] <= v < edges[i + 1]`, except that the last bin is closed on the right, so `v == edges[-1]` counts in the last bin. Values outside `[edges[0], edges[-1]]` are ignored. Do not call `np.histogram`.

### Hints

<details>
<summary>Hint 1</summary>

The edges split the range into pieces of equal width, so `np.linspace` gives them. The half-open rule means a value sitting exactly on an inner edge goes to the bin on its right.

</details>

<details>
<summary>Hint 2</summary>

`np.searchsorted(edges, x, side="right") - 1` gives the bin index of every value in one step. The maximum value then needs to be moved from the nonexistent bin past the end into the last bin.

</details>

<details>
<summary>Hint 3</summary>

Freedman-Diaconis uses the IQR instead of the standard deviation, so a few extreme values do not stretch the bins.

</details>

## Theory

### The simple version

Sorting a pile of exam scores into buckets is a histogram. Buckets that are ten points wide show the general shape. Buckets one point wide show which individual scores happened to occur, mostly noise. Buckets thirty points wide show almost nothing. Rules like Sturges' and Freedman-Diaconis' are recipes for a sensible bucket size from how many scores there are and how spread out they are.

### The formula

**Sturges' rule** chooses the number of bins from the sample size $n$ alone:

$$
k = \lceil \log_2 n \rceil + 1
$$

It assumes roughly bell-shaped data and tends to use too few bins for large or skewed samples.

**Freedman-Diaconis rule** chooses the bin width from the data's spread:

$$
h = \frac{2\,\mathrm{IQR}(x)}{n^{1/3}}, \qquad k = \left\lceil \frac{\max x - \min x}{h} \right\rceil
$$

The interquartile range $\mathrm{IQR} = Q_3 - Q_1$ ignores the extremes, so outliers do not widen the bins.

**Equal-width edges** for $k$ bins over $[a, b]$ are $e_i = a + i\,(b - a)/k$ for $i = 0, \dots, k$.

**Counting.** Value $v$ falls in bin $i$ when $e_i \le v < e_{i+1}$, with the last bin also including its right edge so that the maximum is counted.

### Why the bin count changes the story

A distribution with two peaks needs enough bins to resolve the valley between them. A rule that is right for one dataset can hide structure in another, so trying two or three bin counts before trusting a picture is ordinary practice. A histogram is also only one estimate of a density, and the choice of where the first edge sits can change its look, which is one reason `04-kernel-density` smooths the picture instead.

### Counts versus density

Plotting raw counts makes histograms of different sample sizes incomparable. Dividing each count by $n \times$ (bin width) gives a density whose bars have total area one, which can be overlaid on a theoretical curve or on another sample.

### How NumPy/PyTorch actually implements this

`np.histogram(x, bins=k)` and `np.histogram_bin_edges(x, bins='auto')` compute the counts and edges, and `bins='sturges'` or `bins='fd'` select the two rules built here. `matplotlib.pyplot.hist` and `seaborn.histplot` call the same machinery and draw it. `torch.histc` and `torch.histogram` do the counting on tensors.

## Explanation

`sturges_bins` is `ceil(log2(n)) + 1`. `freedman_diaconis_bins` takes the 25th and 75th percentiles, forms the width `2 * IQR / n^(1/3)` and divides the data range by it, rounding up with `ceil` and never returning less than one, falling back to Sturges' count when the IQR is zero because the width would be zero. `bin_edges` is `np.linspace(min, max, n_bins + 1)`. `histogram_counts` finds each value's bin with `np.searchsorted(side="right") - 1`, moves values equal to the last edge into the last bin, discards values outside the range, and tallies the rest with `np.bincount` using `minlength` so empty bins appear as zeros.
