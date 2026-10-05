---
name: data-science-seaborn-heatmaps-correlation
title: Heatmaps & Correlation Matrices
tags: [data-science, visualization, seaborn, heatmap, correlation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A correlation matrix is the one table every analyst builds on day one: for every pair of numeric columns, how strongly do they move together? It is also hard to read as a grid of numbers once there are more than five columns. A **heatmap** turns each number into a colour, so strong relationships jump out. But a heatmap can mislead as easily as it can reveal: if the colour scale is not pinned to the same range as the data, a correlation of 0.2 can look as strong as 0.9, and a matrix drawn in full shows every pair _twice_, since correlation is symmetric.

This question builds the whole path: compute the matrix, draw it with a scale that always runs from -1 to 1 and is centred on 0, hide the redundant half with a mask, and write the numbers in the cells so the colours can be checked.

### From theory to code

Implement `correlation_matrix(df)`, `heatmap_axes(corr, annotate)`, `upper_triangle_mask(n)` and `masked_heatmap(corr)`. The signatures and docstrings are already in the editor.

### Constraints

- `correlation_matrix(df)` returns the Pearson correlation matrix of the **numeric** columns of `df` (text and boolean columns are left out) as a DataFrame with the column names as both index and columns.
- `heatmap_axes(corr, annotate)` draws `corr` with `sns.heatmap`: colour map `"coolwarm"`, the colour scale fixed to run from `-1` to `1` (`vmin=-1`, `vmax=1`) and centred at `0`, square cells. If `annotate` is true every cell shows its value formatted with two decimals (`".2f"`). Returns the `Axes`.
- `upper_triangle_mask(n)` returns an `n × n` boolean NumPy array that is `True` strictly **above** the diagonal and `False` on and below it.
- `masked_heatmap(corr)` is `heatmap_axes(corr, annotate=True)` with the cells above the diagonal hidden by that mask (so only the diagonal and the lower triangle are drawn and annotated). Returns the `Axes`.
- Use seaborn for the drawing. Do not call `plt.show()`.

### Hints

<details>
<summary>Hint 1</summary>

`df.select_dtypes("number").corr()` computes the matrix for the numeric columns.

</details>

<details>
<summary>Hint 2</summary>

`sns.heatmap` takes `vmin`, `vmax`, `center`, `cmap`, `annot`, `fmt`, `square` and a `mask` where `True` means 'do not draw this cell'.

</details>

<details>
<summary>Hint 3</summary>

`np.triu(np.ones((n, n), dtype=bool), k=1)` is the triangle above the diagonal.

</details>

## Theory

### The simple version

A correlation matrix is a multiplication table for "do these two columns rise and fall together?" A heatmap paints each cell: red for a strong positive link, blue for a strong negative one, white for none. The painting only tells the truth if white always means 0 and the deepest red always means +1, so the colour scale is pinned, not left to match whatever numbers happen to be in the table.

### The number in each cell

The Pearson correlation of columns $x$ and $y$ is

$$
r_{xy} = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i (x_i-\bar{x})^2}\ \sqrt{\sum_i (y_i-\bar{y})^2}} \in [-1, 1]
$$

$r=1$ means a perfect rising straight line, $r=-1$ a perfect falling one, and $r=0$ no _linear_ relationship (a curve can have $r=0$ and still be a perfect relationship). The matrix is symmetric, $r_{xy}=r_{yx}$, and its diagonal is all ones.

### Pinning the colour scale

By default seaborn stretches the colours over the min and max of the data. For correlations that is misleading: a matrix whose largest off-diagonal value is 0.3 would be painted as strongly as one reaching 0.95. `vmin=-1, vmax=1, center=0` with a _diverging_ colormap (`coolwarm`) makes colour mean the same thing in every heatmap.

### Hiding the redundant half

Because $r_{xy}=r_{yx}$, the upper triangle repeats the lower. A mask removes it:

```python
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)   # True above the diagonal
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f")
```

`k=1` starts the triangle one step above the diagonal, so the diagonal itself stays. With $n$ columns that hides $n(n-1)/2$ cells and leaves $n(n+1)/2$.

### Annotations

`annot=True` writes each value into its cell, `fmt=".2f"` rounds it to two decimals. Annotations let a reader check a colour against a number, and they are text objects on the Axes, so they can be read back too.

### How seaborn actually implements this

`heatmap` builds a `_HeatMapper`, which turns the matrix into a masked array, chooses the normalisation from `vmin/vmax/center`, and draws it with `Axes.pcolormesh` (a `QuadMesh` in `ax.collections[0]`, whose `get_array()` holds the values). Masked cells are masked entries in that array and get no annotation. Row and column names become tick labels.

## Explanation

`correlation_matrix` keeps the numeric columns and calls `.corr()`. `heatmap_axes` calls `sns.heatmap` with the diverging colormap, a fixed `-1` to `1` scale centred at zero, square cells and, when asked, two-decimal annotations. `upper_triangle_mask` uses `np.triu` on a matrix of ones with `k=1`, so the diagonal is excluded. `masked_heatmap` passes that mask to the heatmap, so cells above the diagonal are neither drawn nor annotated.
