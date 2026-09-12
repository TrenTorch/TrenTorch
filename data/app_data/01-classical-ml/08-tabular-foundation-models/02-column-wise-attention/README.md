---
name: tabular-foundation-models-column-wise-attention
title: 'Column-wise attention over table cells'
tags: [tabular-foundation-models, attention]
difficulty: Advanced
---

## Statement

Implement:

```python
def column_wise_attention(table, w_query, w_key, w_value) -> np.ndarray:
    """Same mechanism as row_wise_attention, transposed to attend across rows within a column."""
```

- Reuse `01-row-wise-attention`'s `scaled_dot_product_attention`.

## Theory

`01-row-wise-attention` let cells _within one row_ attend to each other, feature interactions within a single data sample. But a table has a second, equally important axis: a whole _column_ is one feature across every sample, and there's real information in how one sample's value in a column compares to every other sample's value in that same column, is this row's age unusually high compared to the rest of the dataset, is this row's price an outlier for its column.

Column-wise attention runs the identical mechanism, just along the other axis: for one column, its `n_rows` cells (that feature's value across every sample) are the sequence attention runs over, one sample's value in a column can be influenced by every other sample's value in the _same column_, but never a different column.

```text
row-wise attention:    within a row, across its columns   (feature interactions per sample)
column-wise attention: within a column, across its rows   (this sample vs. the rest of the dataset, per feature)
```

Both directions matter for genuinely understanding a table: row-wise attention alone can't tell a row "you're unusual for this dataset," and column-wise attention alone can't tell a row "your combination of feature values matters." `03-combine-two-way-attention`, the next question, runs both.

## Explanation

`column_wise_attention` transposes `table`'s first two axes (`np.swapaxes(table, 0, 1)`), turning `(n_rows, n_cols, d_model)` into `(n_cols, n_rows, d_model)`, columns become the leading "batch" dimension and rows become the sequence being attended over, the exact same shape `row_wise_attention` expects, just with rows and columns swapped. Projecting and calling `scaled_dot_product_attention` on this transposed table runs attention within each column exactly the way `row_wise_attention` ran it within each row. `np.swapaxes(attended, 0, 1)` transposes back to the original `(n_rows, n_cols, d_model)` layout before returning, so the caller sees the same shape it passed in either way.
