---
name: sheet-valid-sudoku
title: 'Valid Sudoku Board'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
theory: checking-rules-with-sets
---

## Statement

`board` is a 9 by 9 grid. Each cell is a digit from `1` to `9`, or `0` for an empty cell. Return `True` if the filled cells **do not break the Sudoku rules**: no digit appears twice in any row, any column, or any of the nine `3 x 3` boxes.

You only check the digits that are already there. The board does not have to be solvable.

### Examples

**Example 1**

Input:

```python
valid_sudoku([[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]])
```

Output:

```text
True
```

No digit repeats in any row, column or box.

**Example 2**

Input:

```python
valid_sudoku([[8, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]])
```

Output:

```text
False
```

The top-left `8` repeats in its column (and in its box with the `8` below).

### Constraints

- `board` has 9 rows of 9 cells.
- Each cell is an integer from `0` to `9`.

## Explanation

For every non-empty cell build the three keys for its row, column and box, and put them in `seen`. If a key is already present, the digit repeats in that group and the answer is `False`. The loop covers all `81` cells exactly once.

### Complexity

- Time: O(1). A fixed 81 cells, each checked with three set lookups (O(N^2) for an `N x N` board).
- Space: O(1). At most 243 keys.
