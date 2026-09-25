---
name: numpy-practical-broadcasting-patterns
title: Practical Broadcasting Patterns
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions applying broadcasting to realistic, ML-adjacent tasks: normalizing rows, computing pairwise differences, and applying a per-column scale factor.

## Theory

**Per-row normalization** — subtract each row's own mean, divide by its own std, applied via broadcasting:

```python
row_means = data.mean(axis=1, keepdims=True)     # shape (2, 1)
row_stds = data.std(axis=1, keepdims=True)         # shape (2, 1)
normalized = (data - row_means) / row_stds
```

`keepdims=True` keeps the result at `(2, 1)` instead of collapsing to `(2,)` — `(2, 1)` broadcasts against `(2, 3)` correctly (stretching the trailing size-1 dimension), while `(2,)` would try to align against the trailing `3` and fail.

**Pairwise differences** — using the row-vector/column-vector stretching pattern:

```python
diffs = a[np.newaxis, :] - b[:, np.newaxis]     # shape (len(b), len(a))
```

**Per-column scale factor** — a row-shaped array broadcasts down every row automatically:

```python
scaled = matrix * scale     # scale shape (3,) broadcasts against (4, 3)
```

## Explanation

`normalize_rows` computes `data.mean(axis=1, keepdims=True)` and `data.std(axis=1, keepdims=True)`, then `(data - row_means) / row_stds` in one broadcasted expression. `pairwise_differences` returns `a[np.newaxis, :] - b[:, np.newaxis]`. `scale_columns` returns `matrix * scale_factors` directly, since `scale_factors`'s shape already aligns with the trailing column dimension.
