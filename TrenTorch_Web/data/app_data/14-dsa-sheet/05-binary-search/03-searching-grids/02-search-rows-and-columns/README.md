---
name: sheet-search-rows-and-columns
title: 'Search a Row- and Column-Sorted Matrix'
tags: [dsa-sheet, binary-search, searching-grids]
difficulty: Advanced
theory: cutting-a-long-thin-grid
---

## Statement

Each **row** of `matrix` is sorted in increasing order, and each **column** is sorted in increasing order too (but a row does not have to start after the previous one ends). Return `True` if `target` is in the matrix.

### Examples

**Example 1**

Input:

```python
search_matrix_ii([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 5)
```

Output:

```text
True
```

**Example 2**

Input:

```python
search_matrix_ii([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 15)
```

Output:

```text
False
```

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 2 * 10**5`
- Every row and every column is sorted in increasing order.
- `-10**9 <= matrix[i][j], target <= 10**9`
- The big tests count how many cells you read.

## Explanation

Binary search the middle row of the current block for the first value `>= target`. If it equals `target`, done. Otherwise the target can only be in the block above-right of that spot or the block below-left of it: everything above and to the left is smaller than the target, and everything below and to the right is larger. Search those two smaller blocks the same way; when the block is wider than tall, cut along the middle row, otherwise along the middle column.

This takes `O(m log(2n / m))` reads for a matrix with `m` lines on the shorter side. It beats the simple staircase walk, which costs `O(r + c)`, whenever the matrix is far from square (a single row costs only `log c`).

### Complexity

- Time: O(m log(2n / m)) with m = min(r, c) and n = max(r, c). Binary search the middle line of the shorter side; the answer can only be in two smaller blocks, which leaves `m` lines to search in total, each costing `log` of its share of the longer side.
- Space: O(log m). The recursion is `log m` deep.
