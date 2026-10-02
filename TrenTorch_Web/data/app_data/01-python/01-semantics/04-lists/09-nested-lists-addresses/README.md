---
name: python-lists-nested-lists-addresses
title: Nested Lists and Addresses Across Levels
tags: [python-lists, mutation]
difficulty: Advanced
---

## Statement

Implement functions that build, inspect, and transform lists of lists, using `id()` to verify whether rows are shared or independent.

## Theory

A **nested list** is a list whose elements are themselves lists — a two-level nested list is commonly used as a grid: `grid[i][j]` reads row `i`, then column `j`. `grid[1]` is the address stored in the outer list's slot `1`; `grid[1][0]` reads slot `0` of that row object. `grid[1][0] = 99` mutates the row; `grid[1] = [7, 8]` mutates the outer list by storing a new row address.

**The repeated-row trap.** Repetition with `*` copies addresses, not objects:

```python
bad = [[0, 0]] * 3
bad[0][0] = 5     # all three "rows" show [5, 0] -- they're the same object
```

The fix is a comprehension, whose expression is evaluated once per iteration:

```python
good = [[0, 0] for _ in range(3)]
```

**Copying nested lists.** `grid.copy()` and `grid[:]` are shallow — the new outer list stores the same row addresses. A deep copy creates new rows too.

**Transposing** swaps rows and columns: entry `[i][j]` moves to `[j][i]`. For a rectangular matrix with `r` rows and `c` columns, the result has `c` rows and `r` columns.

**Where this matters later.** Two-dimensional data is the entry point to NumPy arrays and tensors. The repeated-row trap is the reason a matrix of independent rows must be built explicitly.

## Explanation

`make_grid` uses a nested comprehension (`[[fill for _ in range(cols)] for _ in range(rows)]`), never `[[fill] * cols] * rows` or `[[fill] * cols for _ in range(rows)]`'s outer half alone — the whole point is that the _outer_ comprehension's expression (an inner list literal) runs once per row, building a genuinely new list object each time, which is exactly the repeated-row trap's fix. `rows_are_independent` compares `id()` values via a set (`len(ids) == len(set(ids))`) rather than comparing rows with `==`, since two independent rows that happen to hold equal values must still count as independent — only shared addresses should return `False`.
