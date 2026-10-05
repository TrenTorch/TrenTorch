---
name: data-science-seaborn-relational-plots
title: Relational Plots: scatterplot & lineplot
tags: [data-science, visualization, seaborn, relational]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plotting `y` against `x` is the starting point, and seaborn's two relational functions differ in what they assume about the data. `scatterplot` assumes every row is its own observation and draws one dot per row. `lineplot` assumes that **x is something that repeats**: several rows share the same x (several measurements per day, several runs per setting), so it _aggregates_: it draws the mean of y at each x, and by default a band around it showing how much the repeats disagree.

The third dial is `hue`: map a categorical column to colour and the groups separate on the same axes, with a legend that says which colour is which. This question builds a coloured scatter, a mean line, and a mean line with an uncertainty band, and checks each against the numbers it should show.

### From theory to code

Implement `scatter_by_group(df, x, y, hue, hue_order)`, `mean_line(df, x, y)` and `line_with_band(df, x, y)`. The signatures and docstrings are already in the editor.

### Constraints

- `scatter_by_group(df, x, y, hue, hue_order)` draws one scatter point per row of `df` at `(x, y)`, coloured by the value of the column `hue`, with the legend entries in `hue_order`. Returns the `Axes`.
- `mean_line(df, x, y)` draws **one line** whose points are the **mean of `y` at each distinct `x`**, in ascending `x`, with **no uncertainty band**. Returns the `Axes`.
- `line_with_band(df, x, y)` draws the same mean line **with a band** equal to the mean plus and minus **one sample standard deviation** (divide by `n - 1`) of `y` at each `x`. Returns the `Axes`.
- Use seaborn (`sns.scatterplot`, `sns.lineplot`). Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`sns.scatterplot(data=df, x=..., y=..., hue=..., hue_order=...)` draws one point per row and a legend.

</details>

<details>
<summary>Hint 2</summary>

`sns.lineplot` aggregates repeated x values by default. Its `errorbar` argument chooses the band: `None` for no band, `"sd"` for one standard deviation.

</details>

<details>
<summary>Hint 3</summary>

Each call returns the `Axes` it drew on.

</details>

## Theory

### The simple version

A scatter plot is a pin per row. A line plot is what you get when several rows share an x: instead of a zig-zag through all the pins, you draw the **average height at each x** and, optionally, a ribbon showing the spread of the pins around that average. Colouring the pins by a category separates the groups without making a second chart.

### Scatter or line?

| Situation                                             | Plot                                   |
| ----------------------------------------------------- | -------------------------------------- |
| each row is an independent observation                | `scatterplot`                          |
| x repeats (time points, settings), you want the trend | `lineplot` (aggregates)                |
| one row per x already                                 | either; `lineplot` just joins the dots |

### What `lineplot` computes

For each distinct $x$ it takes the set $Y_x = \{y_i : x_i = x\}$ and plots

$$
\bar{y}(x) = \frac{1}{|Y_x|}\sum_{y\in Y_x} y
$$

With `errorbar="sd"` the band is $\bar{y}(x) \pm s(x)$, with the sample standard deviation

$$
s(x) = \sqrt{\frac{1}{|Y_x|-1}\sum_{y\in Y_x}\bigl(y-\bar{y}(x)\bigr)^2}
$$

The default `errorbar=("ci", 95)` is different in meaning: it is a bootstrapped confidence interval for the **mean**, which shrinks as you add data, whereas a standard deviation describes the **spread of the data** and does not.

### Hue

`hue="g"` maps each distinct value of `g` to a colour from the current palette and adds a legend titled `g`. `hue_order` fixes which value gets which colour and the order of the legend, which matters when two charts must use the same colours for the same groups.

### What is on the Axes

A scatter is **one** `PathCollection` holding all the points, with a colour per point. A line plot is `Line2D` objects for the means and a `PolyCollection` for each band, so `ax.lines` and `ax.collections` separate "the trend" from "the uncertainty".

### How seaborn actually implements this

`scatterplot` and `lineplot` build a `_RelationalPlotter`, which maps `hue`/`size`/`style` variables to visual properties (`_HueMapping`), aggregates repeated x values with an `EstimateAggregator` (mean plus the chosen error bar), and then calls `Axes.plot` or `Axes.scatter` and `fill_between`. The legend is built from the mappings, so its entries always agree with the colours actually drawn.

## Explanation

`scatter_by_group` calls `scatterplot` with `hue` and `hue_order`, producing one collection of all points with a colour per group and a legend in the requested order. `mean_line` calls `lineplot` with `errorbar=None`, so seaborn averages `y` at each distinct `x` and draws just the mean line. `line_with_band` calls it with `errorbar="sd"`, which adds a band of one sample standard deviation around that mean.
