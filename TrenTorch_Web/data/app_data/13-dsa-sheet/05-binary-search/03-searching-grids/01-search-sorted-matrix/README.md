---
name: sheet-search-sorted-matrix
title: 'Search a Sorted Matrix'
tags: [dsa-sheet, binary-search, searching-grids]
difficulty: Intermediate
---

## Statement

Each **row** of `matrix` is sorted in increasing order, and the first value of each row is **bigger than the last value of the row above**. So reading the rows one after another gives one sorted list. Return `True` if `target` is in the matrix.

### Examples

**Example 1**

Input:

```python
search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3)
```

Output:

```text
True
```

**Example 2**

Input:

```python
search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13)
```

Output:

```text
False
```

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 2 * 10**5`
- Rows are sorted and each row starts after the previous one ends.
- `-10**9 <= matrix[i][j], target <= 10**9`
- The big tests count how many cells you read.

## Theory

Reading the rows in order gives **one sorted list** of `rows * cols` values. You do not have to build that list: you can **pretend** it exists by converting a position `p` in the imaginary list into a cell: row `p // cols`, column `p % cols`.

Then run an ordinary binary search over positions `0 .. rows * cols - 1`, reading each probe with `matrix[p // cols][p % cols]`. That is `O(log(rows * cols))` reads, instead of looking at every cell.

Mapping a 2D structure onto a 1D index with `//` and `%` is a very common trick for grids, and it works because the rows are all the same length.

## Explanation

An empty matrix (no rows, or rows with no cells) cannot contain the target. Otherwise binary search positions between `0` and `rows * cols - 1`; each probe reads one cell with the division and remainder mapping and compares it with `target`.
