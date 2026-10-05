---
name: data-science-matplotlib-figure-axes-lines
title: Figures, Axes & Line Plots
tags: [data-science, visualization, matplotlib]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every matplotlib chart is a small tree of objects. A **Figure** is the canvas. It holds one or more **Axes**, each of which is one plotting area with its own x and y axis. Each Axes holds the things drawn on it: **Line2D** objects for lines, patches for bars, collections for scatter points, **Text** for labels. When you write `plt.plot(...)` you are using a shortcut that quietly creates a Figure and an Axes for you and draws into "the current one". That is fine for a notebook cell and a recipe for confusing bugs in a function that draws more than one chart.

This question uses the _object_ interface, where you hold the Figure and the Axes yourself and call methods on them. Because a chart is a tree of objects with numbers inside, you can read those numbers back, which is also how it is tested: no pixels, just `ax.lines[0].get_ydata()`.

### From theory to code

Implement `line_chart(x, y, title, xlabel, ylabel)`, `add_line(ax, x, y, label, color)`, `line_data(ax)` and `style_line(line, color, linestyle, linewidth, marker)`. The signatures and docstrings are already in the editor.

### Constraints

- Create figures with `plt.subplots()` and draw through the returned `Axes`. Do not call `plt.show()`.
- `line_chart` returns `(fig, ax)`: a new `Figure` with exactly one `Axes` holding exactly one line through the points `(x, y)`, with the given title, x label and y label, and the grid switched on.
- `add_line` draws one more line on `ax` through `(x, y)` with the given `label` and `color`, shows a legend listing the **labelled** lines, and returns the new `Line2D`.
- `line_data(ax)` returns a list with one `(xs, ys)` pair for every line on `ax`, in drawing order, where `xs` and `ys` are Python lists of numbers.
- `style_line(line, color, linestyle, linewidth, marker)` changes those four properties of an existing line (it does not draw a new one) and returns the line.

### Hints

<details>
<summary>Hint 1</summary>

`plt.subplots()` returns a `(figure, axes)` pair. `ax.plot(x, y)` returns a list of lines, so `line, = ax.plot(...)` unpacks the one you made.

</details>

<details>
<summary>Hint 2</summary>

Lines created without a `label` are left out of the legend automatically.

</details>

<details>
<summary>Hint 3</summary>

Every property you can pass to `plot` has a `set_` method on the line: `set_color`, `set_linestyle`, `set_linewidth`, `set_marker`.

</details>

## Theory

### The simple version

A matplotlib figure is a picture frame (Figure) holding one or more windows (Axes). Each window has its own x ruler and y ruler, and the things you draw sit inside it: a line is an object with its own colour and thickness, a title is a text object. `ax.plot` creates a line object and hands you a handle to it, which you can keep and change later. That is the whole idea of the object interface: **create, keep the handle, change the object**.

### The object tree

```
Figure
 └─ Axes                  (one plotting area)
     ├─ XAxis, YAxis      (ticks, tick labels, axis label)
     ├─ lines   : Line2D  (ax.plot)
     ├─ patches : Rectangle ... (ax.bar, ax.hist)
     ├─ collections       (ax.scatter)
     ├─ texts   : Text    (ax.text, ax.annotate)
     └─ legend  : Legend
```

`ax.lines`, `ax.patches`, `ax.collections` and `ax.texts` are plain lists you can read, which is why a test can check a chart without looking at it.

### Two interfaces

|             | pyplot (`plt.plot`)                        | object-oriented (`ax.plot`)               |
| ----------- | ------------------------------------------ | ----------------------------------------- |
| Which Axes? | "the current one", global state            | the one you hold                          |
| Good for    | quick exploration                          | functions, multi-panel figures, libraries |
| Risk        | draws on the wrong axes after another call | none: you name the target                 |

The object-oriented style is what every plotting library built on matplotlib (seaborn, pandas `.plot`) expects.

### Line properties

A `Line2D` stores `xdata`, `ydata`, `color`, `linestyle` (`"-"`, `"--"`, `":"`), `linewidth` in points, `marker` (`"o"`, `"s"`, `"^"`) and `label`. Colours can be names (`"red"`), hex (`"#1f77b4"`) or cycle references (`"C0"`), and `matplotlib.colors.to_hex` converts any of them to one canonical form.

### Legends and labels

`ax.legend()` collects every artist that has a label **not starting with an underscore**. Unlabelled lines get an automatic `_childN` label, which is why they stay out of the legend.

### How matplotlib actually implements this

`ax.plot` builds `Line2D` artists and adds them to `ax.lines`, updating the data limits so autoscaling can run. Nothing is rasterised until the figure is drawn (`fig.savefig`, `plt.show`, or `fig.canvas.draw()`), so you can build and inspect a figure without ever rendering it, using the `Agg` (raster, no window) backend.

## Explanation

`line_chart` makes the figure and axes with `plt.subplots()`, plots one line, sets the title and both labels, turns the grid on and returns the pair. `add_line` plots with the given colour and label, shows the legend (which lists only labelled lines) and returns the new line object. `line_data` reads each `Line2D` back with `get_xdata` and `get_ydata` and converts them to plain lists. `style_line` calls the four setters on the existing line, so no new line is added.
