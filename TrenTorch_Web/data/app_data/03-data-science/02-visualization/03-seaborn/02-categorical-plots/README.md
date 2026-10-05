---
name: data-science-seaborn-categorical-plots
title: Categorical Plots: barplot & countplot
tags: [data-science, visualization, seaborn, categorical]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Two questions dominate categorical charts, and they look alike. "**How many** rows are in each category?" is a count, and `countplot` draws it. "**What is the average** of a number in each category?" is a summary, and `barplot` computes it and draws it. Mixing them up is easy because both produce bars, and because `barplot` quietly draws error bars unless told not to, so a bar chart of means is also a chart of uncertainty whether you asked or not.

The other decision is order. Seaborn lists categories in the order they first appear in the data, which is usually accidental. Putting them in a deliberate order (alphabetical, or ranked by value) is what makes a chart readable, and this question builds both the ranking and the charts that use it.

### From theory to code

Implement `ranked_order(df, cat, value)`, `mean_bars(df, cat, value, order)`, `count_bars(df, cat, hue, order, hue_order)` and `horizontal_means(df, cat, value, order)`. The signatures and docstrings are already in the editor.

### Constraints

- `ranked_order(df, cat, value)` returns the categories of `cat` as a list, ordered by the **mean** of `value` from largest to smallest, ties by category name ascending. Missing values of `value` are ignored in the mean.
- `mean_bars(df, cat, value, order)` draws one bar per category in `order`, whose height is the mean of `value` in that category, **without error bars**. Returns the `Axes`.
- `count_bars(df, cat, hue, order, hue_order)` draws, for each category in `order`, one bar per value in `hue_order` whose height is the number of rows with that category and hue. Returns the `Axes`.
- `horizontal_means(df, cat, value, order)` is `mean_bars` drawn **horizontally**: categories on the y axis in `order` (top to bottom), the mean as the bar length on the x axis, no error bars. Returns the `Axes`.
- Use seaborn for the drawing. Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`df.groupby(cat)[value].mean()` gives the means. Sort by `(-mean, name)` to get the ranked order.

</details>

<details>
<summary>Hint 2</summary>

`sns.barplot(..., estimator="mean", errorbar=None, order=...)` draws means without error bars. `sns.countplot(..., hue=...)` draws counts.

</details>

<details>
<summary>Hint 3</summary>

A horizontal bar plot swaps the roles: put the numeric column on `x` and the category on `y`.

</details>

## Theory

### The simple version

A countplot is a tally sheet: one bar per category, as tall as the pile of rows in it. A barplot is a report card: one bar per category, as tall as the average mark. Both are bars; one _counts rows_ and the other _summarises a number_. If the bars should be in a sensible order (best first), you must say so, because the default is "whichever appeared first".

### Counting vs summarising

|            | `countplot`          | `barplot`                                    |
| ---------- | -------------------- | -------------------------------------------- |
| Needs      | a category column    | a category and a numeric column              |
| Bar height | rows in the category | `estimator` of the numbers (mean by default) |
| Error bars | none                 | a bootstrapped 95% interval by default       |

For a category $c$ with rows $R_c$ the two heights are

$$
\text{count}_c = |R_c|, \qquad \text{mean}_c = \frac{1}{|R_c|}\sum_{i\in R_c} y_i
$$

### Error bars

`barplot`'s default `errorbar=("ci", 95)` resamples each category 1000 times to estimate how uncertain the mean is, which draws line objects on top of the bars. `errorbar=None` turns that off, leaving only the bars, which is what you want when the numbers themselves matter and when the picture must be reproducible (the bootstrap is random).

### Order

Seaborn takes categories in order of first appearance in the column. `order=[...]` sets the order explicitly, and for `hue` the `hue_order`. A ranked order, largest mean first, makes comparisons read top to bottom (or left to right):

```python
order = df.groupby("team")["score"].mean().sort_values(ascending=False).index
```

Break ties by name, otherwise tied categories can swap places between runs.

### Orientation

Seaborn infers the orientation from which axis holds the numbers. Numbers on `x` and the category on `y` gives horizontal bars, which is the better layout for long category names that would overlap under a vertical chart.

### How seaborn actually implements this

`barplot` and `countplot` build a `_CategoricalPlotter` that maps each category to a position `0..n-1`, computes the statistic per category (and per hue level) with an `EstimateAggregator`, and then calls matplotlib's `Axes.bar` or `barh`. The bars are the patches in the Axes, grouped in one `BarContainer` per hue level, which is how a test can read one series at a time.

## Explanation

`ranked_order` averages `value` per category, sorts by mean descending and then by name, and returns the names. `mean_bars` is `barplot` with `estimator="mean"`, `errorbar=None` and the explicit `order`. `count_bars` is `countplot` with `hue`, `order` and `hue_order`; seaborn draws one bar container per hue level, each holding one bar per category. `horizontal_means` puts the numeric column on `x` and the category on `y`, which makes the bars horizontal and puts the categories on the vertical axis in the given order.
