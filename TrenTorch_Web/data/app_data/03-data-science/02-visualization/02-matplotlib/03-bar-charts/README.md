---
name: data-science-matplotlib-bar-charts
title: Bar Charts: Simple, Grouped & Stacked
tags: [data-science, visualization, matplotlib, bar]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A bar chart compares quantities across categories, and it is the chart most often drawn wrongly. Matplotlib does not know that your x values are categories: it places each bar at a numeric **position** (0, 1, 2, ...) and you then tell it what text to print under each position. A _grouped_ chart puts several bars side by side inside one category, so each bar's position has to be shifted by hand. A _stacked_ chart puts bars on top of each other, so each bar needs to know where the one below it ends.

The geometry is simple but unforgiving, and since every bar is a `Rectangle` with an `x`, a `width`, a `y` (its bottom) and a `height`, you can check every one of them. This question builds the three charts and the labelling step that puts each value on top of its bar.

### From theory to code

Implement `bar_chart(labels, values)`, `grouped_bars(labels, series)`, `stacked_bars(labels, series)` and `annotate_bars(ax)`. The signatures and docstrings are already in the editor.

### Constraints

- `labels` is a list of `n` category names; `values` and each list in `series` have `n` non-negative numbers. `series` is a dict mapping a series name to its list of `n` values; iterate it in insertion order.
- `bar_chart(labels, values)` returns `(fig, ax)`: bars **centred at positions `0..n-1`**, each of width `0.8` (the default), x tick positions `0..n-1` labelled with `labels`, and the bottom of the y axis at `0`.
- `grouped_bars(labels, series)` returns `(fig, ax)`. With `k` series, each bar has width `0.8 / k`. Bar `j` of group `i` is centred at `i + (j - (k - 1) / 2) * width`. Ticks are at `0..n-1` labelled with `labels`. The legend lists the series names.
- `stacked_bars(labels, series)` returns `(fig, ax)`. Every series draws bars of width `0.6` centred at `0..n-1`; the bar of series `j` starts (`y`) where the bars of the series before it end. Ticks and legend as above.
- `annotate_bars(ax)` writes the height of every bar (`ax.patches`) as text, formatted with `f"{height:g}"`, centred horizontally above the top of that bar (`y + height`), and returns the list of those strings in the order of `ax.patches`.

### Hints

<details>
<summary>Hint 1</summary>

`ax.bar(x, height, width=..., bottom=...)` takes numeric positions. Tick labels are a separate step: `set_xticks` then `set_xticklabels`.

</details>

<details>
<summary>Hint 2</summary>

For grouped bars, the offset of series `j` from the group centre is `(j - (k - 1) / 2) * width`, which centres the whole group on its tick.

</details>

<details>
<summary>Hint 3</summary>

For stacked bars, keep a running array of bottoms and add each series' values to it after drawing.

</details>

## Theory

### The simple version

Bars stand on a numbered shelf: shelf 0, shelf 1, shelf 2. Matplotlib only knows shelf numbers; the names under the shelves are a second, separate instruction. Grouped bars share one shelf by standing side by side; stacked bars share it by standing on each other's heads.

### Anatomy of a bar

`ax.bar(x, h, width, bottom)` creates one `Rectangle` per bar and stores them in `ax.patches`:

| Property       | Meaning                                    |
| -------------- | ------------------------------------------ |
| `get_x()`      | the **left edge** (centre minus width/2)   |
| `get_width()`  | width                                      |
| `get_y()`      | the bottom (`0`, or the `bottom` argument) |
| `get_height()` | height                                     |

So a bar's centre is `p.get_x() + p.get_width() / 2` and its top is `p.get_y() + p.get_height()`.

### Grouped bars

With $k$ series in a group of total width $0.8$, each bar gets width $w = 0.8/k$ and series $j$ sits at offset

$$
\delta_j = \left(j - \frac{k-1}{2}\right) w
$$

from the category's position, which spreads the $k$ bars symmetrically around it.

### Stacked bars

The bottom of series $j$ at category $i$ is the cumulative height below it:

$$
b_{j,i} = \sum_{m<j} v_{m,i}
$$

Stacking is only meaningful for quantities that add up to a whole (revenue by product), not for averages.

### Honest axes

A bar's _length_ encodes the value, so the axis must start at zero or the picture exaggerates differences. That is why the first test is `ylim` starting at 0, and why bar charts are a poor fit for data that can be negative without extra care.

### Labelling

`ax.text(x, y, s, ha="center", va="bottom")` puts text in data coordinates, so anchoring a label at `(centre, top)` keeps it attached to its bar even if the axes are later rescaled. Putting numbers on bars removes the need to read them off the axis.

### How matplotlib actually implements this

`Axes.bar` builds a list of `Rectangle` patches, wraps them in a `BarContainer` (kept in `ax.containers`, which is what `ax.bar_label` uses) and adds them to `ax.patches`. Categories are an illusion: with string x values matplotlib converts them to 0, 1, 2, ... through a _category unit converter_, which is the same thing done by hand here.

## Explanation

`bar_chart` draws bars at integer positions, sets ticks there with the labels and pins the bottom of the y axis at zero. `grouped_bars` computes the bar width `0.8 / k` and shifts each series by `(j - (k - 1) / 2) * width` around the tick. `stacked_bars` draws each series with `bottom` equal to the running total of the series before it, then adds the series to that total. `annotate_bars` reads each patch's centre and top and writes its height there, returning the formatted strings in patch order.
