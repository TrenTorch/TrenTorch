---
name: data-science-seaborn-distribution-plots
title: Distributions: histplot, kdeplot & ecdfplot
tags: [data-science, visualization, seaborn, distributions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Seaborn is matplotlib with the statistics built in. You hand it a table and the names of columns, and it does the grouping, binning and smoothing before drawing. For one numeric column it offers three views of the same distribution: a **histogram** (counts in bins), a **kernel density estimate** (a smooth curve that integrates to 1) and an **empirical CDF** (the fraction of values at or below each point, with no binning at all).

Each is a function that draws on an `Axes` and returns it, so everything it drew can be read back: the bar heights, the curve, the labels. The details of what _scale_ each one uses (counts, density or proportion) is exactly the sort of thing that changes a picture's meaning, so this question builds all three, plus a comparison of one distribution per group on a fair, per-group scale.

### From theory to code

Implement `histogram_axes(df, column, bins, stat)`, `kde_axes(df, column)`, `kde_by_group(df, column, group, order)` and `ecdf_axes(df, column)`. The signatures and docstrings are already in the editor.

### Constraints

- Draw with seaborn (`import seaborn as sns`), passing `data=df` and the column names, and **return the `Axes`** the call returns. Do not call `plt.show()`.
- `histogram_axes(df, column, bins, stat)` draws a histogram of `column` with `bins` bins and the statistic `stat` (`"count"`, `"density"` or `"probability"`).
- `kde_axes(df, column)` draws one kernel density curve of `column`.
- `kde_by_group(df, column, group, order)` draws one density curve per value of `group`, in the colour order given by `order` (a list of the group values), **each curve normalised on its own** (so every curve integrates to 1 whatever the group size).
- `ecdf_axes(df, column)` draws the empirical cumulative distribution function of `column`.

### Hints

<details>
<summary>Hint 1</summary>

`sns.histplot`, `sns.kdeplot` and `sns.ecdfplot` all take `data=` and `x=`. `histplot` has `bins` and `stat`.

</details>

<details>
<summary>Hint 2</summary>

`hue=` splits a plot by a column, `hue_order=` fixes which value gets which colour, and `common_norm=False` normalises each hue level separately.

</details>

<details>
<summary>Hint 3</summary>

Each call returns the `Axes` it drew on.

</details>

## Theory

### The simple version

Three ways to describe where a pile of numbers sits. A **histogram** counts how many fall in each bucket. A **density curve** blurs each number into a small hill and adds the hills up into one smooth skyline whose total area is 1. An **ECDF** walks along the number line and, at each point, reports "what fraction of the data is at or below here?" Same data, three honest views, and each has a different y axis.

### Scales, because they decide the picture

| Plot                           | Y axis      | Meaning                     |
| ------------------------------ | ----------- | --------------------------- |
| `histplot(stat="count")`       | Count       | number of values in the bin |
| `histplot(stat="density")`     | Density     | bar areas sum to 1          |
| `histplot(stat="probability")` | Probability | bar heights sum to 1        |
| `kdeplot`                      | Density     | curve area is 1             |
| `ecdfplot`                     | Proportion  | rises from 0 to 1           |

Counts depend on the sample size and the bin width; density and the curves do not, which is what lets two groups of different sizes be compared.

### The density estimate

A kernel density estimate places a small bell (a Gaussian) on every observation $x_i$ and averages them:

$$
\hat{f}(x) = \frac{1}{n h}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right), \qquad \int \hat{f}(x)\,dx = 1
$$

The bandwidth $h$ is the width of each bell. Too small gives a spiky curve that traces the sample; too large smooths real structure away. Seaborn picks $h$ with Scott's rule, $h \approx 1.06\,\hat\sigma\,n^{-1/5}$.

### The empirical CDF

$$
\hat{F}(x) = \frac{1}{n}\sum_{i=1}^{n}\mathbf{1}[x_i \le x]
$$

It jumps by $1/n$ at every observation, needs no binning and no bandwidth, and can be read directly: the value where it crosses 0.5 is the median.

### Several groups

`hue="group"` draws one curve per group. With the default `common_norm=True` all curves share a single normalisation, so a group with twice as many rows has a curve with twice the area, which hides shape. `common_norm=False` normalises each separately, which is what you want when comparing _shapes_. Seaborn draws hue levels in the reverse of `hue_order` in the line list, so identify curves by colour or legend, not by position.

### How seaborn actually implements this

`histplot`, `kdeplot` and `ecdfplot` build a `_DistributionPlotter` that computes the statistic (`np.histogram`, a Gaussian KDE, a cumulative sum) with the `stats` module, then draws it using matplotlib bars, lines and `fill_between` on the target Axes. Everything is an ordinary matplotlib artist, so `ax.patches` and `ax.lines` hold exactly what was drawn.

## Explanation

Each function is a single seaborn call on the data frame, returning the Axes. `histogram_axes` passes `bins` and `stat` to `histplot`, whose bars use NumPy's bin edges and the requested scale. `kde_axes` calls `kdeplot` for one density curve. `kde_by_group` adds `hue` and `hue_order` and sets `common_norm=False` so each group's curve is normalised separately and integrates to one. `ecdf_axes` calls `ecdfplot`, which draws the step function from 0 to 1.
