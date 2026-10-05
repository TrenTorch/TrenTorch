---
name: data-science-plotly-figure-traces-layout
title: Figures, Traces & Layout
tags: [data-science, visualization, plotly]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Plotly draws in a browser, so a plotly figure is not a picture. It is a **description**: a plain structure, a list of `data` (the _traces_, each one a scatter, a bar, a heatmap) and a `layout` (titles, axes, legend, size), which the plotly.js library in the browser turns into pixels. That is why a figure can be saved as JSON, sent anywhere, and rebuilt, and why it is interactive for free: hover, zoom and toggling a trace in the legend are plotly.js features working from the description.

The consequence for code is pleasant: building a figure is building a structure, and every property is addressable by a path like `fig.layout.xaxis.title.text`. This question builds a figure from scratch with `plotly.graph_objects`, adds a second trace, reads the structure back, sets axis ranges, and round-trips the whole figure through JSON.

### From theory to code

Implement `line_figure(x, y, name, title, xlabel, ylabel)`, `add_series(fig, x, y, name, color)`, `trace_summaries(fig)`, `set_axis_ranges(fig, xrange, yrange)` and `json_roundtrip(fig)`. The signatures and docstrings are already in the editor.

### Constraints

- Use `plotly.graph_objects` (`import plotly.graph_objects as go`). Do not call `fig.show()`.
- `line_figure` returns a new `go.Figure` with **one** `Scatter` trace through `(x, y)` drawn with `mode="lines+markers"` and the given `name`, with the layout title `title`, x axis title `xlabel` and y axis title `ylabel`.
- `add_series(fig, x, y, name, color)` adds one more `Scatter` trace (lines only, `mode="lines"`) to `fig` with that `name` and line colour, and returns the **same** figure object.
- `trace_summaries(fig)` returns a list with one dict per trace, in order: `{"name": ..., "type": ..., "n_points": ...}`, where `type` is the trace type (such as `"scatter"`) and `n_points` is the number of `x` values.
- `set_axis_ranges(fig, xrange, yrange)` fixes the visible range of the x axis and of the y axis (each a `[low, high]` pair) and returns the same figure.
- `json_roundtrip(fig)` serialises the figure to a JSON string and rebuilds a **new** figure from it with `plotly.io`, which it returns.

### Hints

<details>
<summary>Hint 1</summary>

`go.Figure(data=[go.Scatter(...)])` builds a figure; `fig.update_layout(title=..., xaxis_title=..., yaxis_title=...)` sets the layout; `fig.add_trace(...)` appends a trace.

</details>

<details>
<summary>Hint 2</summary>

`fig.update_xaxes(range=[...])` and `fig.update_yaxes(range=[...])` set axis ranges.

</details>

<details>
<summary>Hint 3</summary>

`plotly.io.to_json(fig)` and `plotly.io.from_json(text)` are a matched pair.

</details>

## Theory

### The simple version

A plotly figure is a recipe card, not a photograph. The card lists the ingredients (traces: this line, that bar) and the presentation (layout: titles, axes, colours). A browser is the kitchen that cooks it. Because it is just a card, you can photocopy it (JSON), mail it, edit one line of it, and hand it to another kitchen.

### The two halves

```
Figure
 ├─ data   : [ Scatter(...), Bar(...), ... ]   one object per trace
 ├─ layout : title, xaxis, yaxis, legend, width, ...
 └─ frames : [ ... ]                           (only for animations)
```

A **trace** has a `type` (`scatter`, `bar`, `heatmap`, `histogram`...) and properties specific to the type: `x`, `y`, `mode`, `name`, `marker`, `line`. The **layout** holds everything about the chart as a whole. Every property has a documented path, and the objects validate what you assign: a misspelled property raises an error immediately instead of silently doing nothing.

### Building and changing

| Task                         | Call                                                       |
| ---------------------------- | ---------------------------------------------------------- |
| create a trace               | `go.Scatter(x=..., y=..., mode="lines+markers", name="a")` |
| put it in a figure           | `go.Figure(data=[trace])` or `fig.add_trace(trace)`        |
| set titles, size, legend     | `fig.update_layout(title=..., xaxis_title=...)`            |
| change every x axis          | `fig.update_xaxes(range=[0, 10])`                          |
| change traces after the fact | `fig.update_traces(line_color="red")`                      |

`update_*` methods return the figure itself, so calls can be chained. `mode` combines `lines`, `markers` and `text` with `+`.

### Reading a figure back

`fig.data` is a tuple of trace objects, `fig.layout` the layout object. Attributes read like Python attributes: `fig.data[0].x`, `fig.layout.xaxis.title.text`. Arrays you passed in come back as NumPy arrays or tuples, so wrap them in `list(...)` before comparing. `fig.to_dict()` gives the raw structure, but long numeric arrays may be stored in a compact binary form there, so prefer the properties.

### Serialisation

```python
import plotly.io as pio
text = pio.to_json(fig)        # a JSON string
copy = pio.from_json(text)     # an equal, independent figure
```

This is what lets a figure built in Python render in a notebook, a web page or a dashboard.

### How plotly actually implements this

`graph_objects` classes are generated from plotly.js's schema: each property has a validator that checks type and allowed values at assignment. The Python side never draws anything; `fig.show()` or `fig.to_html()` ships the JSON to plotly.js, which does the rendering and the interactivity.

## Explanation

`line_figure` creates one `Scatter` with `lines+markers` and the name, then sets the title and axis titles with `update_layout`. `add_series` appends a lines-only `Scatter` with the line colour and returns the same figure. `trace_summaries` reads each trace's name, type and number of `x` values. `set_axis_ranges` uses `update_xaxes` and `update_yaxes` with the given ranges. `json_roundtrip` writes the figure to a JSON string with `plotly.io.to_json` and rebuilds a new figure from it with `from_json`.
