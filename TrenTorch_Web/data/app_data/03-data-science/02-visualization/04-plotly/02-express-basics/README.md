---
name: data-science-plotly-express-basics
title: Plotly Express: Scatter, Bar, Line & Histogram
tags: [data-science, visualization, plotly, express]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Building a figure trace by trace is flexible and wordy. **Plotly Express** (`px`) is the short way: you give it a DataFrame and column names and it creates the traces, the axis titles, the legend and a sensible colour scheme in one call. `px.scatter(df, x="height", y="weight", color="species")` produces one trace _per species_, named, coloured and listed in the legend, because a column mapped to `color` means "split by this".

Because Express builds ordinary plotly figures, everything it produced can be checked: how many traces, what each is called, what numbers each holds. The decisions that matter are the same as in any chart: which order the groups come in, whether to aggregate before drawing, and whether lines are sorted along the x axis. This question builds four Express charts and pins down each of those.

### From theory to code

Implement `scatter_by_group(df, x, y, group, order)`, `total_bars(df, cat, value)`, `histogram_figure(df, column, bins)` and `lines_by_group(df, x, y, group)`. The signatures and docstrings are already in the editor.

### Constraints

- Use `plotly.express` (`import plotly.express as px`). Do not call `fig.show()`.
- `scatter_by_group(df, x, y, group, order)` returns a scatter with **one trace per value** of `group`, the traces in the order given by `order` (a list of the group values), each trace holding that group's points (rows in their original order).
- `total_bars(df, cat, value)` returns a bar chart with **one bar per category**: the **sum** of `value` per category, **largest total first**, ties by category name ascending. Aggregate with pandas first, then draw.
- `histogram_figure(df, column, bins)` returns a histogram of `column` requesting `bins` bins (`nbinsx`).
- `lines_by_group(df, x, y, group)` returns a line chart with **one line per group**, groups in order of their first appearance in `df`, each line's points **sorted by `x` ascending**.

### Hints

<details>
<summary>Hint 1</summary>

Mapping a column to `color=` creates one trace per value. `category_orders={"group": [...]}` fixes their order.

</details>

<details>
<summary>Hint 2</summary>

`px.bar` draws exactly the rows it is given, so group and sort the data first.

</details>

<details>
<summary>Hint 3</summary>

`px.line` joins points in the order of the rows, so sort by `x` within each group before drawing.

</details>

## Theory

### The simple version

`graph_objects` is a box of Lego bricks; Plotly Express is the pre-built kit that takes a table and the names of the columns, and assembles a finished chart. Say which column is x, which is y, and which should split into colours, and the kit works out the rest.

### What Express decides for you

| Argument                              | Effect                                                                 |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `x`, `y`                              | which columns go on the axes (axis titles are set to the column names) |
| `color`                               | split into **one trace per value**, each coloured, with a legend       |
| `facet_col` / `facet_row`             | one panel per value (next questions)                                   |
| `category_orders`                     | the order of categories and of traces                                  |
| `nbins`, `barmode`, `hover_data`, ... | chart-specific options                                                 |

The return value is a normal `go.Figure`, so `fig.data`, `fig.layout` and every `update_*` method work as before.

### One trace per group

`px.scatter(df, x="x", y="y", color="g")` internally splits the frame by `g` and creates one `Scatter` per value, each holding only that group's rows and named after the value. Which comes first is decided by `category_orders` if you give it, otherwise by first appearance.

### Aggregate first

`px.bar(df, x="team", y="score")` draws **one bar per row** (stacked if a team has several rows), it does not sum or average. To chart totals, aggregate in pandas:

```python
totals = df.groupby("team", as_index=False)["score"].sum()
totals = totals.sort_values(["score", "team"], ascending=[False, True])
px.bar(totals, x="team", y="score")
```

### Lines follow the row order

`px.line` connects points in the order they appear in the frame, so unsorted data produces a zig-zag. Sort by the x column (within each group) before drawing.

### Histograms

`px.histogram(df, x="v", nbins=10)` bins in the browser; `nbins` is a _request_ (plotly.js rounds to "nice" bin edges), recorded in the trace as `nbinsx`. The y axis title is `count` by default.

### How Express actually implements this

`px` functions are one generic routine (`make_figure`) that takes the arguments, splits the DataFrame into groups according to the mappings (`color`, `symbol`, `facet_*`), creates one graph-object trace per group with the right properties, and sets the layout (axis titles from column names, legend title from the colour column). It returns that figure; nothing is Express-specific afterwards.

## Explanation

`scatter_by_group` maps `group` to `color` with `category_orders` so the traces come out in the requested order. `total_bars` sums `value` per category with pandas, sorts by total descending and then name, and passes the result to `px.bar`, which draws one bar per row. `histogram_figure` calls `px.histogram` with `nbins`, which Express records on the trace as `nbinsx`. `lines_by_group` sorts the data by `x` and calls `px.line` with `color=group`; the groups come out in order of first appearance and each line's points are in ascending `x`.
