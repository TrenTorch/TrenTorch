---
name: tabular-foundation-models-row-wise-attention
title: 'Row-wise attention over table cells'
tags: [tabular-foundation-models, attention]
difficulty: Advanced
---

## Statement

Implement:

```python
def softmax(x, axis=-1) -> np.ndarray: ...
def scaled_dot_product_attention(query, key, value) -> np.ndarray: ...
def row_wise_attention(table, w_query, w_key, w_value) -> np.ndarray: ...
```

- `table` represents a whole data table already embedded into vectors: shape `(n_rows, n_cols, d_model)`, one `d_model`-dimensional vector per cell (one sample's one feature value).
- `row_wise_attention` runs attention _within_ each row, across that row's own cells, never mixing information between different rows.

## Theory

Every model in this curriculum before this track processes a table's rows as fixed-length feature vectors and learns one set of weights that treats every column the same way for every row (a linear model's `weight`, a tree's fixed splits). TabPFN-style tabular foundation models take a different approach: treat the table itself as the input to a Transformer-style attention mechanism, letting the model learn, per table, which cells should influence which.

**Attention**, the core mechanism, computes a weighted average of `value` vectors, where the weights come from how well each `query` matches each `key`:

```text
scores  = query @ key^T / sqrt(d_k)     # how well does each query match each key
weights = softmax(scores, axis=-1)      # turn scores into a probability distribution per query
output  = weights @ value               # weighted average of values, per query
```

Dividing by `sqrt(d_k)` (the key dimension) keeps the dot products from growing too large as dimensionality increases, which would otherwise push `softmax` into a near-one-hot regime and make gradients vanish, a real, deliberate stabilization, not an arbitrary constant.

**Row-wise attention** applies exactly this mechanism _within_ each row of the table: for one row, its `n_cols` cells are the sequence attention runs over, one cell can attend to (be influenced by) every other cell in the _same row_, but never a cell in a different row. This lets the model learn feature interactions _within_ one data sample, "does a high value in column A matter more when column B is also high," entirely from the data, the same thing a decision tree's split structure hard-codes by hand, learned instead through attention weights.

## Explanation

`softmax` subtracts the max along `axis` before exponentiating (the same stability trick `04-gaussian-mixture`'s E-step uses for its own log-sum-exp), then divides by the sum along that same axis, so probabilities sum to `1` along whichever axis represents "the choices being weighted."

`scaled_dot_product_attention` computes `query @ np.swapaxes(key, -1, -2)`, transposing only the last two axes so this works correctly whether there's a leading batch dimension (like `row_wise_attention`'s `n_rows`) or not, divides by `sqrt(d_k)`, `softmax`s over the last axis (over keys, one weight per key for each query), then `weights @ value` for the final weighted average.

`row_wise_attention` projects the whole `table` with each weight matrix (`table @ w_query` broadcasts the `(d_model, d_model)` matrix across every row and cell at once), then calls `scaled_dot_product_attention` on the three projections directly, NumPy's batched matrix multiplication (`@` on arrays with more than 2 dimensions) automatically keeps the `n_rows` dimension separate throughout, which is exactly what makes every row's attention computation independent of every other row's, without an explicit Python loop over rows.
