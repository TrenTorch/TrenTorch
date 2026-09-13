---
name: tabular-foundation-models-column-wise-attention
title: 'Column-wise attention over table cells'
tags: [tabular-foundation-models, attention]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-row-wise-attention` let cells _within one row_ attend to each other, feature interactions within a single data sample. But a table has a second, equally important axis: a whole _column_ is one feature across every sample, and there's real information in how one sample's value in a column compares to every other sample's value in that same column — is this row's age unusually high compared to the rest of the dataset, is this row's price an outlier for its column.

### From theory to code

Implement `column_wise_attention(table, w_query, w_key, w_value)`: same mechanism as `row_wise_attention`, transposed to attend across rows within a column. Reuse `01-row-wise-attention`'s `scaled_dot_product_attention`.

### Constraints

- `table`: shape `(n_rows, n_cols, d_model)`. Returns the same shape.
- Cell `(i, c)` may attend to any other cell in _column_ `c` (any row, same column), never a cell in a different column.
- Works correctly for a non-square table (`n_rows != n_cols`).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.swapaxes(table, 0, 1)` turns `(n_rows, n_cols, d_model)` into `(n_cols, n_rows, d_model)` — now columns are the leading "batch" dimension and rows are the sequence, exactly the shape `row_wise_attention`'s own mechanism expects.

</details>

<details>
<summary>Hint 2</summary>

After running the same projection-and-attention steps on the transposed table, swap the same two axes back before returning — otherwise the output shape won't match the input's `(n_rows, n_cols, d_model)` layout.

</details>

## Theory

### The simple version

Column-wise attention runs the identical mechanism as row-wise attention, just along the other axis: for one column, its `n_rows` cells (that feature's value across every sample) are the sequence attention runs over — one sample's value in a column can be influenced by every other sample's value in the _same column_, but never a different column.

### The formula

```text
row-wise attention:    within a row, across its columns   (feature interactions per sample)
column-wise attention: within a column, across its rows   (this sample vs. the rest of the dataset, per feature)
```

Both directions matter for genuinely understanding a table: row-wise attention alone can't tell a row "you're unusual for this dataset," and column-wise attention alone can't tell a row "your combination of feature values matters." `03-two-way-attention-block`, the next question, runs both.

### How PyTorch actually implements this

Context only, untested by your submission: this is the same scaled dot-product attention mechanism as `01-row-wise-attention`, applied along a transposed axis — TabPFN and similar tabular transformer architectures alternate row-wise and column-wise attention blocks in exactly this way, letting the model learn both per-sample feature interactions and per-feature cross-sample comparisons.

## Explanation

`column_wise_attention` transposes `table`'s first two axes (`np.swapaxes(table, 0, 1)`), turning `(n_rows, n_cols, d_model)` into `(n_cols, n_rows, d_model)` — columns become the leading "batch" dimension and rows become the sequence being attended over, the exact same shape `row_wise_attention` expects, just with rows and columns swapped. Projecting and calling `scaled_dot_product_attention` on this transposed table runs attention within each column exactly the way `row_wise_attention` ran it within each row. `np.swapaxes(attended, 0, 1)` transposes back to the original `(n_rows, n_cols, d_model)` layout before returning, so the caller sees the same shape it passed in either way.
