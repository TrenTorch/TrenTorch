---
name: data-science-plotly-subplots-facets
title: Subplots & Facets
tags: [data-science, visualization, plotly, subplots]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A single plot answers one question; plotting a measurement and the quantity that drives it **one above the other, sharing the same time axis**, answers a better one: "when the price moved, what did volume do?" Plotly builds such multi-panel figures with `make_subplots`, which creates a grid of panels, each with its own pair of axes, and lets you say which trace goes in which cell and which axes line up.

The second tool is the **facet**: the same chart repeated for each value of a column. Express makes it one argument (`facet_col="region"`), and seeing whether a pattern holds in every panel is the reason to do it. Panels are numbered in a way that surprises people (the axes of the second panel are `x2`/`y2`), and the panel titles are _annotations_, so everything is checkable.

### From theory to code

Implement `stacked_panels(x, y_top, y_bottom, titles)`, `facet_scatter(df, x, y, col, col_order)` and `panel_titles(fig)`. The signatures and docstrings are already in the editor.

### Constraints

- `stacked_panels(x, y_top, y_bottom, titles)` returns a `go.Figure` made with `make_subplots` with **2 rows and 1 column**, **sharing the x axis**, with `titles` (a pair) as the subplot titles. Row 1 holds one `Scatter` of `(x, y_top)` and row 2 one `Scatter` of `(x, y_bottom)`.
- `facet_scatter(df, x, y, col, col_order)` returns a Plotly Express scatter faceted by the column `col`, **one panel per value in `col_order`, left to right**.
- `panel_titles(fig)` returns the text of the subplot or facet titles, **in the order they appear in the figure's annotations**, as a list of strings.
- Do not call `fig.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=[...])` creates the grid; `fig.add_trace(trace, row=1, col=1)` puts a trace in a cell.

</details>

<details>
<summary>Hint 2</summary>

`px.scatter(..., facet_col="col", category_orders={"col": [...]})` creates the facet panels.

</details>

<details>
<summary>Hint 3</summary>

Subplot and facet titles are stored as annotations in `fig.layout.annotations`.

</details>

## Theory

### The simple version

A multi-panel figure is a page divided into boxes. Each box has its own rulers, but you can tell some boxes to _share a ruler_ so that what happens at the same time lines up vertically. A facet is the same box photocopied once per group.

### `make_subplots`

```python
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=["Price", "Volume"])
fig.add_trace(go.Scatter(x=x, y=price), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=volume), row=2, col=1)
```

The grid has `rows × cols` cells. Each trace is placed with `row=` and `col=`; plotly then records which axes it uses.

### How axes are numbered

Panels count in reading order, and each owns a pair of axes whose names are numbered the same way:

| Panel  | x axis | y axis | In the layout                    |
| ------ | ------ | ------ | -------------------------------- |
| first  | `x`    | `y`    | `layout.xaxis`, `layout.yaxis`   |
| second | `x2`   | `y2`   | `layout.xaxis2`, `layout.yaxis2` |
| third  | `x3`   | `y3`   | `layout.xaxis3`, ...             |

A trace stores the axes it belongs to as `trace.xaxis` and `trace.yaxis` (`"x2"`, `"y2"`), and the first panel's are the default (`"x"`, `"y"`).

### Sharing an axis

`shared_xaxes=True` links the x axes of the panels in a column, so zooming one zooms all. In the layout that is the property `matches`: the upper panel's axis gets `xaxis.matches == "x2"`, pointing at the bottom panel's axis, which keeps the tick labels. The redundant tick labels on the upper panel are hidden.

### Facets in Express

`px.scatter(df, x="x", y="y", facet_col="region")` creates a panel per value of `region` (`facet_row` for rows), shares the axes, and titles each panel `region=north`. Panel order follows `category_orders`, otherwise first appearance.

### Titles are annotations

Subplot and facet titles are not part of the axes: they are text _annotations_ positioned above each panel, stored in `fig.layout.annotations`, one per panel. Reading `annotation.text` gives the title.

### How plotly actually implements this

`make_subplots` calculates the position of every cell (as fractions of the figure, the `domain` of each axis), creates the numbered axes in the layout with those domains, and remembers the grid in a private `_grid_ref`. `add_trace(..., row, col)` looks up the axis names for that cell and sets `xaxis`/`yaxis` on the trace.

## Explanation

`stacked_panels` builds a two-row grid that shares the x axis and carries the two titles, then adds each series to its own row; the second panel's trace therefore uses axes `x2`/`y2`, and the top panel's x axis is linked to it. `facet_scatter` calls Express with `facet_col` and `category_orders`, which produces one panel per value in the requested order and titles each `col=value`. `panel_titles` reads the text of every annotation in order, which is where plotly stores those titles.
