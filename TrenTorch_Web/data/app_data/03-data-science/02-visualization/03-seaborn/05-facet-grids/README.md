---
name: data-science-seaborn-facet-grids
title: Figure-level Plots: displot, catplot & pairplot
tags: [data-science, visualization, seaborn, facets]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Everything so far drew onto **one** Axes. Seaborn has a second family of functions, the **figure-level** ones (`displot`, `catplot`, `relplot`, `pairplot`), that create the whole figure themselves and return a grid object. Their reason to exist is _faceting_: the same plot repeated for each value of a column (`col="region"`), all with the same scales, so a pattern that holds in every panel is visibly real. `pairplot` is faceting taken to the limit: every numeric column against every other.

These functions differ in practice from the axes-level ones in two ways that matter. They return a **grid** (`FacetGrid`, `PairGrid`) whose `.axes` array you index, and they own the figure, so you cannot pass them an `ax=`. This question builds the three most useful: histograms per group, bars per group, and a scatter matrix.

### From theory to code

Implement `histograms_by_group(df, value, col, col_order, bins)`, `bars_by_group(df, x, y, col, col_order)` and `pair_scatter(df, variables)`. The signatures and docstrings are already in the editor.

### Constraints

- `histograms_by_group(df, value, col, col_order, bins)` returns a `FacetGrid` with one panel per value in `col_order` (left to right), each a histogram of `value` for that group's rows with `bins` bins. Use `sns.displot`.
- `bars_by_group(df, x, y, col, col_order)` returns a `FacetGrid` with one panel per value of `col` in `col_order`, each a bar chart of the **mean** of `y` for each category of `x`, **without error bars**. Use `sns.catplot` with `kind="bar"`. The categories of `x` appear in the order of their first occurrence.
- `pair_scatter(df, variables)` returns a `PairGrid` with `len(variables)` rows and columns for exactly those numeric columns, in that order. Use `sns.pairplot` with `vars=variables`.
- Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`sns.displot(data=df, x=..., col=..., col_order=..., bins=...)` returns a `FacetGrid`; its `.axes` array has one panel per column value.

</details>

<details>
<summary>Hint 2</summary>

`sns.catplot(..., kind="bar", errorbar=None, col=...)` is the figure-level version of `barplot`.

</details>

<details>
<summary>Hint 3</summary>

`sns.pairplot(df, vars=[...])` draws every pair, with distributions on the diagonal.

</details>

## Theory

### The simple version

Draw one chart, then photocopy it once per group onto a single sheet, all with the same rulers. If the bump is in the same place on every sheet, it is real; if it only shows up on one, that group is special. A pairplot photocopies a scatter for every pair of columns, so you can survey all the relationships at once.

### Two families of seaborn functions

|                           | axes-level                           | figure-level                                |
| ------------------------- | ------------------------------------ | ------------------------------------------- |
| Examples                  | `histplot`, `barplot`, `scatterplot` | `displot`, `catplot`, `relplot`, `pairplot` |
| Draws on                  | an `Axes` you may pass (`ax=`)       | a new figure it creates                     |
| Returns                   | the `Axes`                           | a `FacetGrid` / `PairGrid`                  |
| Faceting (`col=`, `row=`) | no                                   | yes                                         |

A figure-level function wraps an axes-level one: `displot(kind="hist")` calls `histplot` on each panel, `catplot(kind="bar")` calls `barplot`.

### The grid object

`g = sns.displot(...)` gives a `FacetGrid`:

| Attribute     | Content                                    |
| ------------- | ------------------------------------------ |
| `g.axes`      | 2D array of Axes, shape `(n_rows, n_cols)` |
| `g.axes.flat` | the panels in reading order                |
| `g.figure`    | the `Figure`                               |
| panel titles  | `"col = value"`                            |

By default panels **share axes** (`sharex=True, sharey=True`), which is the entire point: equal scales make the panels comparable.

### Order of the panels

Seaborn puts panels in the order values first appear in the column, which is rarely what you want. `col_order=[...]` fixes it. The same holds for `order` on the category axis of `catplot`.

### Pair plots

`sns.pairplot(df, vars=[a, b, c])` returns a `PairGrid` with `len(vars)` rows and columns. Row $i$, column $j$ plots `vars[j]` on x against `vars[i]` on y; the diagonal shows each variable's own distribution. With $k$ variables there are $k(k-1)$ scatter panels, symmetric in content, which is why `corner=True` can show only the lower half.

### How seaborn actually implements this

A `FacetGrid` creates the figure and a grid of Axes with `plt.subplots(nrows, ncols, sharex=True, sharey=True)`, subsets the data per panel, and calls the plotting function on each with the subset. The figure-level functions are thin wrappers that translate their arguments into those calls.

## Explanation

`histograms_by_group` calls `displot` with `col` and `col_order`, which builds a one-row grid and draws a histogram with `bins` bins of each group's rows on a shared scale. `bars_by_group` uses `catplot` with `kind="bar"` and `errorbar=None`, which is `barplot` in every panel and gives the mean of `y` per category of `x`. `pair_scatter` calls `pairplot` with `vars`, which returns a `PairGrid` with one row and one column per variable.
