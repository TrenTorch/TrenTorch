---
name: data-science-matplotlib-subplots-shared-axes
title: Subplots, Shared Axes & Twin Axes
tags: [data-science, visualization, matplotlib, subplots]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

One chart answers one question. A set of **small multiples**, the same chart repeated once per group, answers "does the pattern hold in every group?", and it only works if the panels use the **same scales**. Panels with their own free axes look similar when the data are wildly different, and different when the data are almost the same. Sharing the axes is what makes the eye's comparison valid.

A second, related tool is the **twin axis**: two quantities with different units (revenue in euros and a conversion rate in percent) drawn against one x axis, each with its own y scale on opposite sides. It is easy to misuse, so the colour of each axis label should match its line.

This question builds a grid of panels with shared axes (and hides the panels left over), a twin-axis chart, and a helper that sets limits, ticks and scale in one place.

### From theory to code

Implement `small_multiples(series, ncols)`, `twin_axis_chart(x, y_left, y_right, left_label, right_label)` and `set_limits_and_ticks(ax, xlim, ylim, xticks, xticklabels, logy)`. The signatures and docstrings are already in the editor.

### Constraints

- `small_multiples(series, ncols)` takes a dict mapping a panel title to an `(x, y)` pair, and returns `(fig, axes)`, where `axes` is a 2D NumPy array of shape `(nrows, ncols)` with `nrows = ceil(len(series) / ncols)`. Panel `i` (row-major order) draws its line and gets its key as its title. **All panels share both the x and the y axis.** Unused panels are made invisible (`set_visible(False)`).
- `twin_axis_chart` returns `(fig, ax_left, ax_right)`. The left axes plots `y_left` in `"tab:blue"`, the right axes (made with `twinx`, so it shares the x axis) plots `y_right` in `"tab:red"`. Each y label is set from its argument and coloured like its line. The x axis is shared.
- `set_limits_and_ticks(ax, xlim, ylim, xticks, xticklabels, logy)` sets the x and y limits, puts the x ticks at `xticks` with the text `xticklabels`, and switches the y axis to a logarithmic scale if `logy` is true (otherwise linear).
- Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`plt.subplots(nrows, ncols, sharex=True, sharey=True, squeeze=False)` always returns a 2D array of axes, even for one row.

</details>

<details>
<summary>Hint 2</summary>

`ax.twinx()` returns a second Axes on top of the first that shares its x axis and has its own y axis on the right.

</details>

<details>
<summary>Hint 3</summary>

Set the tick _positions_ first (`set_xticks`), then their _text_ (`set_xticklabels`).

</details>

## Theory

### The simple version

A row of thermometers is only comparable if every one is marked in the same degrees and starts at the same place. A grid of small charts is a row of thermometers: share the axes and a taller line really is a bigger number. A twin axis is two thermometers in different units clipped to the same stem; they can only be read together if each is clearly coloured.

### The grid of Axes

`plt.subplots(nrows, ncols)` creates the figure and the whole grid of Axes in one call. With `squeeze=False` the result is always a 2D array, so `axes[r, c]` and `axes.flat` work whatever the shape, which removes the special cases of one row or one column.

### Shared axes

`sharex=True` links the x axes of all panels: they get the same limits, and zooming one zooms all. `sharey=True` does the same for y. Internally the linked axes belong to one _group_, which you can query with `ax1.get_shared_x_axes().joined(ax1, ax2)`. Sharing also hides the redundant tick labels on the inner panels, which saves space.

### More panels than data

With 5 groups in a 2×3 grid there is one empty frame. `ax.set_visible(False)` hides the Axes and everything in it, which keeps the figure tidy without changing the grid shape.

### Twin axes

`ax2 = ax.twinx()` creates a new Axes drawn over the first with the **same x axis** and an independent y axis on the right. The danger is visual: two unrelated curves can be made to look correlated by choosing the two y ranges. Colour-coding the axis label and tick colours to match the line, and labelling the units, is the minimum for honesty.

### Limits, ticks and scales

`set_xlim`/`set_ylim` choose the window; ticks are positions and tick _labels_ are text. A **log scale** (`set_yscale("log")`) makes multiplicative changes look equal, so growth that doubles every year becomes a straight line, but zero and negative values cannot be shown.

### How matplotlib actually implements this

`Figure.subplots` calls `GridSpec` to place the Axes. Sharing is implemented by a `Grouper` that records which axes share a limit, and every `set_xlim` on one member propagates to the others. `twinx` calls `Figure.add_subplot` for an Axes in the same position and links its x axis to the original's.

## Explanation

`small_multiples` computes the number of rows from the number of series and columns, creates the grid with shared x and y and `squeeze=False`, draws each series on its panel with its key as the title, and hides the leftover panels. `twin_axis_chart` plots on the original axes, creates the second with `twinx`, and sets each label colour to match its line. `set_limits_and_ticks` sets the limits, then the tick positions and their labels, and picks the y scale from `logy`.
