---
name: data-science-matplotlib-scatter-colour-size
title: Scatter Plots: Colour, Size & Fits
tags: [data-science, visualization, matplotlib, scatter]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A scatter plot is the honest way to look at two numbers per observation: one dot per row, no line implying that neighbouring dots are connected. Its power is that a dot has more than a position. Its **size** can carry a third number (population, revenue), its **colour** can carry a fourth (a score, a temperature), and a line drawn over the dots can summarise the trend. A reader should be able to tell what each encoding means, which is why a colour scale needs a _colourbar_ and a fitted line needs a label.

This question builds the three layers of a typical scatter figure: the dots with size and colour, a least-squares trend line, and a second layer that marks the points that sit unusually far from the average.

### From theory to code

Implement `scatter_chart(x, y, sizes, values, label)`, `fit_line(ax, x, y)` and `highlight_outliers(ax, x, y, k)`. The signatures and docstrings are already in the editor.

### Constraints

- `scatter_chart` returns `(fig, ax, points)`: a new figure with one scatter of `(x, y)`, marker areas `sizes`, coloured by `values` with the `viridis` colormap, and a **colourbar** whose label is `label`. `points` is the scatter's collection.
- `fit_line(ax, x, y)` computes the ordinary least-squares line `y = slope * x + intercept` through the points and draws it on `ax` as **one line segment from the smallest `x` to the largest `x`**, colour `"red"`, label `"fit"`. It returns `(slope, intercept)` as Python floats.
- `highlight_outliers(ax, x, y, k)` draws, as a **second scatter** on `ax`, the points whose `y` differs from the mean of `y` by more than `k` times the (population) standard deviation of `y`. They are red, with marker area 80. It returns the number of outliers as an `int`. If there are none it draws nothing.
- `x`, `y`, `sizes`, `values` are equal-length sequences of numbers. Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`ax.scatter(x, y, s=sizes, c=values, cmap=...)` returns the collection a colourbar needs: `fig.colorbar(points, ax=ax, label=...)`.

</details>

<details>
<summary>Hint 2</summary>

`np.polyfit(x, y, 1)` returns the slope and intercept of the least-squares line.

</details>

<details>
<summary>Hint 3</summary>

Build a boolean mask for the outliers with NumPy, and count it with `mask.sum()`.

</details>

## Theory

### The simple version

A scatter plot is a map: each observation is a pin at (x, y). Pin size and colour are two more dials that can show two more numbers, and a trend line is a ruler laid across the cloud. Every dial needs a legend or the map cannot be read, so a colour scale gets a colourbar.

### What the collection stores

`ax.scatter` returns a `PathCollection`, one object for all the points (far cheaper than a thousand Line2D objects). From it you can read:

| Method          | Returns                                             |
| --------------- | --------------------------------------------------- |
| `get_offsets()` | the $(x, y)$ positions, shape `(n, 2)`              |
| `get_sizes()`   | marker areas in points²                             |
| `get_array()`   | the values mapped to colour (when `c=` was numbers) |
| `get_cmap()`    | the colormap object, e.g. name `viridis`            |

Marker **area** (`s`) is in points squared, so doubling `s` doubles the _area_, not the width.

### Colour as data

When `c` is a list of numbers, matplotlib normalises them to $[0, 1]$ (from their min to their max) and looks them up in a colormap. A colourbar is the key that explains that mapping and is itself an Axes added to the figure.

### The least-squares line

For points $(x_i, y_i)$ the line minimising $\sum_i (y_i - (a x_i + b))^2$ has

$$
a = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sum_i (x_i-\bar{x})^2}, \qquad b = \bar{y} - a\bar{x}
$$

and `np.polyfit(x, y, 1)` returns $(a, b)$. Drawing it between the smallest and largest $x$ is enough because a straight line is determined by two points.

### Flagging unusual points

A point is unusual when it is more than $k$ standard deviations from the mean:

$$
|y_i - \bar{y}| > k\,\sigma_y
$$

With $\sigma_y$ the population standard deviation (divide by $n$, NumPy's default). It is a quick screen, not a verdict: a single huge value inflates $\sigma_y$ itself and can hide itself.

### How matplotlib actually implements this

A `PathCollection` keeps arrays of offsets, sizes and colour data and draws them in a single call, which is why scatter scales to many points. A `ScalarMappable` (the colour mapping object shared by the collection and the colourbar) holds the normalisation and the colormap, so changing one updates both.

## Explanation

`scatter_chart` calls `ax.scatter` with sizes, values and the `viridis` colormap and adds a colourbar bound to that collection, which creates a second Axes holding the scale and its label. `fit_line` gets the slope and intercept from `np.polyfit(x, y, 1)`, evaluates them at the smallest and largest `x` and draws a single red segment labelled `fit`. `highlight_outliers` computes the mask of points beyond `k` standard deviations of the mean of `y`, draws only those as a second red scatter when there are any, and returns how many.
