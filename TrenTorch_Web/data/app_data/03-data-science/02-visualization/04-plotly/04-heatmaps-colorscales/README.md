---
name: data-science-plotly-heatmaps-colorscales
title: Heatmaps, Colour Scales & Annotations
tags: [data-science, visualization, plotly, heatmap]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A heatmap encodes a matrix as colour, and the whole picture depends on one decision: **how numbers map to colours**. Plotly stretches the colour scale over the data's own minimum and maximum unless told otherwise, so two heatmaps of two different matrices can use "red" to mean different numbers, and a correlation matrix whose largest off-diagonal entry is 0.3 can be painted as vividly as one that reaches 0.95. Pinning the range (`zmin`, `zmax`), centring a diverging scale on zero (`zmid`) and labelling the colourbar make the colours comparable and readable.

Colours alone are imprecise, so the cells that matter get their value written on them. This question builds a general heatmap with an explicit scale, the correlation-matrix heatmap that applies it, and a function that annotates only the cells above a threshold, which is how a reader's eye is guided to the strong relationships.

### From theory to code

Implement `heatmap_figure(z, x_labels, y_labels, title, zmin, zmax, colorscale)`, `correlation_heatmap(df)` and `annotate_strong_cells(fig, z, x_labels, y_labels, threshold)`. The signatures and docstrings are already in the editor.

### Constraints

- Use `plotly.graph_objects`. Do not call `fig.show()`.
- `heatmap_figure` returns a `go.Figure` with one `Heatmap` trace: `z` is the matrix (a list of rows), `x` the column labels, `y` the row labels, the given `colorscale`, colour range `zmin` to `zmax`, a colourbar whose title is `"value"`, and the layout title `title`.
- `correlation_heatmap(df)` returns the heatmap of the **Pearson correlation matrix of the numeric columns** of `df` (labels = column names on both axes), colour scale `"RdBu"`, range fixed to `-1` to `1` and **centred at 0** (`zmid=0`), with every cell labelled with its value to two decimals (`texttemplate="%{z:.2f}"`).
- `annotate_strong_cells(fig, z, x_labels, y_labels, threshold)` adds one annotation for every cell whose **absolute value is at least `threshold`**: the text is the value to two decimals (`f"{v:.2f}"`), positioned at that cell (`x` = its column label, `y` = its row label), without an arrow (`showarrow=False`). It returns the **number of annotations added**, as an `int`.

### Hints

<details>
<summary>Hint 1</summary>

`go.Heatmap(z=..., x=..., y=..., colorscale=..., zmin=..., zmax=..., colorbar=dict(title=dict(text="value")))`.

</details>

<details>
<summary>Hint 2</summary>

`zmid=0` centres a diverging scale at zero. Set `zmin`/`zmax` as well so the range is symmetric.

</details>

<details>
<summary>Hint 3</summary>

`fig.add_annotation(x=..., y=..., text=..., showarrow=False)` places text in data coordinates.

</details>

## Theory

### The simple version

A heatmap is a spreadsheet where the numbers have been replaced by colours. To read it you need the key: which colour means 0 and which means the maximum. If every heatmap makes its own key from its own data, you cannot compare two of them. Fix the key (the colour scale range), put a label on it (the colourbar title), and write the exact figures on the cells you want people to read.

### How a number becomes a colour

Plotly first normalises the value to $[0,1]$ using the colour range, then looks the result up in the colour scale:

$$
t = \frac{z - z_{\min}}{z_{\max} - z_{\min}}, \qquad \text{colour} = \text{scale}(t)
$$

A colour scale is a list of `(position, colour)` stops; names such as `"Viridis"` (sequential) and `"RdBu"` (diverging) are shorthand for such lists.

### Sequential vs diverging

| Data                                    | Scale                            | Why                                   |
| --------------------------------------- | -------------------------------- | ------------------------------------- |
| counts, magnitudes                      | sequential (`Viridis`, `Blues`)  | one direction: low to high            |
| correlations, differences from a target | **diverging** (`RdBu`, `RdYlBu`) | a meaningful midpoint, two directions |

For a diverging scale, `zmid=0` pins the neutral colour to zero. Together with `zmin=-1, zmax=1` it means "white is no correlation, deep red is +1, deep blue is −1" in _every_ correlation heatmap.

### Text on cells

`texttemplate="%{z:.2f}"` writes each cell's value with two decimals inside the cell (plotly.js formatting). For selective labels, annotations are more flexible: an annotation at the cell's data coordinates `(x_label, y_label)` with `showarrow=False` is just text on the plot, and you decide which cells get one.

### The colourbar

`colorbar=dict(title=dict(text="value"))` titles the key. Without it the reader must guess what the colours measure.

### How plotly actually implements this

A `Heatmap` trace keeps `z` (a 2D array) plus `x` and `y` category or numeric positions; plotly.js draws one rectangle per cell and does the colour lookup in the browser. The colour range, `zmid` and the scale are trace properties, so everything above is plain data you can read from `fig.data[0]`.

## Explanation

`heatmap_figure` creates a `Heatmap` with the matrix, the labels, the scale and the explicit colour range, gives the colourbar the title `value` and sets the layout title. `correlation_heatmap` computes the correlation matrix of the numeric columns and builds the same heatmap with `RdBu`, range -1 to 1, `zmid=0` and a two-decimal cell template. `annotate_strong_cells` loops over the cells, adds a text annotation at `(column label, row label)` for every cell whose absolute value reaches the threshold, and counts them.
