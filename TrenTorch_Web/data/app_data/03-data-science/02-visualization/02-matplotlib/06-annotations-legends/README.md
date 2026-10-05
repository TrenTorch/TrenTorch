---
name: data-science-matplotlib-annotations-legends
title: Annotations, Reference Lines & Legends
tags: [data-science, visualization, matplotlib, annotation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A chart that only shows lines makes the reader do the work. The good ones _point_: an arrow at the peak with its value, a dashed line at the target, a shaded band over the period that mattered, a legend that says which colour is which. These extras are cheap to add and are what turn a plot from "data" into "an argument". They are also objects, `Annotation`, `Line2D` and `Polygon` patches, with positions and text you can read back.

This question builds four such touches: an annotated maximum, a horizontal threshold with a label, a shaded span between two x values, and a legend placed _outside_ the plot area so it never hides data.

### From theory to code

Implement `annotate_max(ax, x, y)`, `add_threshold(ax, value, label)`, `shade_region(ax, x0, x1, label)` and `legend_below(ax, title)`. The signatures and docstrings are already in the editor.

### Constraints

- `annotate_max(ax, x, y)` finds the point with the largest `y` (the first one if tied) and adds an annotation whose text is `f"max = {y_max:g}"`, which points at `(x_max, y_max)` with an arrow, with its text placed 20 points above that point (`xytext=(0, 20)`, `textcoords="offset points"`). It returns the `Annotation`.
- `add_threshold(ax, value, label)` draws a horizontal line at `y = value`, colour `"gray"`, linestyle `"--"`, with that label, shows the legend, and returns the line.
- `shade_region(ax, x0, x1, label)` shades the vertical band between `x0` and `x1` with colour `"orange"` and `alpha=0.2` and the given label, and returns the patch.
- `legend_below(ax, title)` shows the legend with that title, centred under the axes (`loc="upper center"`, `bbox_to_anchor=(0.5, -0.15)`) in two columns, and returns the `Legend`.
- `x` and `y` are equal-length numeric sequences. Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`ax.annotate(text, xy=point, xytext=offset, textcoords="offset points", arrowprops=dict(arrowstyle="->"))` creates an `Annotation`. Without `arrowprops` there is no arrow.

</details>

<details>
<summary>Hint 2</summary>

`ax.axhline(y, ...)` is a line across the whole width. `ax.axvspan(x0, x1, ...)` is a shaded vertical band.

</details>

<details>
<summary>Hint 3</summary>

`ax.legend(...)` returns the `Legend` object. `bbox_to_anchor` moves it relative to the axes.

</details>

## Theory

### The simple version

Annotations are sticky notes on a chart: an arrow from a note to the point it talks about. A threshold is a dashed ruler across the page, a shaded region is a highlighter stroke over a period, and the legend is the key in the corner. None of them add data, and all of them add meaning.

### Annotations

`ax.annotate(text, xy, xytext, ...)` draws `text` at `xytext` and, if `arrowprops` is given, an arrow pointing to `xy`. Both positions are in a _coordinate system_ you choose:

| `textcoords`      | `xytext` is                         |
| ----------------- | ----------------------------------- |
| `"data"`          | data coordinates (the same as `xy`) |
| `"offset points"` | an offset in points from `xy`       |
| `"axes fraction"` | a fraction of the axes box          |

Offsetting in **points** keeps the label a fixed distance from its target when the data range changes, which is why it is the usual choice for "put the note just above the peak". `ann.xy` stores the target and `ann.get_text()` the words.

### Lines and spans in data space

`axhline(y)` and `axvline(x)` draw lines that span the other axis completely, in axes-fraction coordinates on that other axis, so they do not change the autoscaling the way `plot` would. `axvspan(x0, x1)` adds a rectangle covering the full height between two x values: the standard way to mark a recession, a campaign period or a test window.

### The legend

A legend gathers every artist with a label. It is an object (`ax.get_legend()`), and its position is set with `loc` (which corner of the legend) and `bbox_to_anchor` (where in the axes to attach it):

```python
ax.legend(title="Series", loc="upper center",
          bbox_to_anchor=(0.5, -0.15), ncol=2)
```

`(0.5, -0.15)` in axes coordinates is centred horizontally and just below the bottom edge, so the legend sits outside the plot and cannot cover data.

### Transparency

`alpha` between 0 and 1 controls opacity. A shaded span at `alpha=0.2` lets the line underneath show through, which is the point of a highlight.

### How matplotlib actually implements this

An `Annotation` is a `Text` subclass that also owns an optional `FancyArrowPatch`. Spans are `Polygon` patches added to `ax.patches`, and axis lines are ordinary `Line2D`s with a blended transform (data on one axis, axes fraction on the other). Legend entries are built from "handles", the artists with labels, each drawn by a small handler that makes a miniature of the artist.

## Explanation

`annotate_max` takes the index of the largest `y`, creates an annotation with the formatted text at that point, offset 20 points up with an arrow, and returns it. `add_threshold` draws a gray dashed horizontal line with the label and calls `legend` so the label is visible. `shade_region` calls `axvspan` with the orange semi-transparent style and the label and returns the patch. `legend_below` calls `legend` with the title, the lower-centre anchor and two columns, and returns the legend object.
