---
name: sheet-maximal-square
title: 'Maximal Square'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
theory: squares-inside-a-grid
---

## Statement

`matrix` holds `0`s and `1`s. Return the **area** of the largest **square** that contains only `1`s.

For `[[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]]` the answer is `4`.

The starter code checks every possible square cell by cell. It is correct but too slow for big matrices.

### Examples

**Example 1**

Input:

```python
maximal_square([[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]])
```

Output:

```text
4
```

**Example 2**

Input:

```python
maximal_square([[0, 1], [1, 0]])
```

Output:

```text
1
```

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Explanation

`prev` holds the previous row of sides and `cur` the row being built. The diagonal value is kept in `diag` since it is overwritten.

### Complexity

- Time: O(r * c). Every cell is computed once from three neighbours.
- Space: O(c). Two rows of the table.
