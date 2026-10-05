---
name: data-science-matplotlib-histograms
title: Histograms with hist, Density & Overlays
tags: [data-science, visualization, matplotlib, histogram]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`ax.hist` is a one-line call that hides three decisions: how the range is cut into bins, whether the bar heights are _counts_ or a _density_, and, when two histograms share a plot, whether they use the **same bins**. Skip the last one and the comparison is meaningless: two samples drawn with different bin edges can look different purely because of where the cuts fell.

Because `hist` also returns the numbers it drew (the counts and the edges), the chart can be checked against `np.histogram` exactly. This question draws a histogram and reads its numbers back, draws a density histogram whose bars have total area 1, and overlays two samples on a shared set of bins so the comparison is fair.

### From theory to code

Implement `draw_histogram(data, bins)`, `density_histogram(data, bins)` and `overlay_histograms(a, b, bins, labels)`. The signatures and docstrings are already in the editor.

### Constraints

- `data`, `a`, `b` are 1D sequences of at least two numbers with at least two distinct values. `bins` is an integer number of bins.
- `draw_histogram(data, bins)` draws on a new `Axes` with `ax.hist` and returns `(fig, ax, counts, edges)` where `counts` and `edges` are the arrays returned by `hist`. There are `bins` bars.
- `density_histogram(data, bins)` returns `(fig, ax)` of a histogram whose bar heights are a **density** (the total area of the bars is 1) and whose y label is `"density"`.
- `overlay_histograms(a, b, bins, labels)` draws both samples on **one** `Axes` using the **same bin edges**, computed from the combined data with `np.histogram_bin_edges(np.concatenate([a, b]), bins=bins)`, each with `alpha=0.5` and its label from `labels` (a pair), shows a legend, and returns `(fig, ax, edges)`.
- Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`ax.hist(data, bins=...)` returns `(counts, edges, patches)`.

</details>

<details>
<summary>Hint 2</summary>

`density=True` rescales the heights so that `sum(height * width) == 1`.

</details>

<details>
<summary>Hint 3</summary>

Passing the _edges array_ as `bins` makes both histograms use exactly those cuts.

</details>

## Theory

### The simple version

Sorting numbers into buckets and stacking blocks in each bucket is a histogram. Whether the blocks are _how many fell in the bucket_ (counts) or _how crowded the bucket is relative to its width_ (density) changes the scale but not the shape. And if you want to compare two crowds, you must use the same buckets for both, otherwise you are comparing the buckets, not the crowds.

### Counts and density

With bin edges $e_0 < e_1 < \dots < e_k$, $n$ values and $c_i$ values in bin $i$:

$$
\text{count}_i = c_i, \qquad \text{density}_i = \frac{c_i}{n\,(e_{i+1}-e_i)}
$$

The density makes the bar _areas_ sum to one:

$$
\sum_i \text{density}_i\,(e_{i+1}-e_i) = \sum_i \frac{c_i}{n} = 1
$$

which lets histograms of different sample sizes (or different bin widths) share an axis, and be laid over a theoretical probability density.

### What `hist` returns

`counts, edges, patches = ax.hist(x, bins=k)`: `counts` has length $k$, `edges` has length $k+1$, and `patches` are the bars (also in `ax.patches`). Each patch's height is the count (or density) and its x is the left edge. Values are binned half-open, $e_i \le v < e_{i+1}$, except that the **last** bin includes its right edge.

### Fair overlays

If `a` and `b` each pick their own `bins=10`, the two sets of edges differ, and bars of different widths are not comparable. Computing the edges once from the combined data, then passing that array to both calls, makes every bar in one histogram line up with a bar in the other. `alpha=0.5` makes the overlap readable.

### How matplotlib actually implements this

`Axes.hist` calls `np.histogram` to compute the counts (so the numbers are NumPy's, exactly), applies the density scaling if asked, then draws one `Rectangle` per bin through `Axes.bar`. The patches are grouped in a `BarContainer`, and an overlay is simply two containers sharing the Axes.

## Explanation

`draw_histogram` calls `ax.hist` and returns the counts and edges it produced, which are the same numbers `np.histogram` computes. `density_histogram` passes `density=True` so bar areas sum to one and labels the y axis `density`. `overlay_histograms` computes one set of edges from both samples together and passes that array as `bins` to two `hist` calls with `alpha=0.5` and their labels, so every bar of one sample lines up with the same bin of the other, then shows the legend.
