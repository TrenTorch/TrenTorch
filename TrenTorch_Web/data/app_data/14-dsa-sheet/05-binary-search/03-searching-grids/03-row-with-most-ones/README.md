---
name: sheet-row-with-most-ones
title: 'Row With the Most Ones'
tags: [dsa-sheet, binary-search, searching-grids]
difficulty: Intermediate
theory: the-row-with-the-most-ones
---

## Statement

Every row of `matrix` contains only `0` and `1`, and each row is **sorted**: all its `0`s come before all its `1`s. Return the **index of the row with the most `1`s**. If several rows tie, return the smallest index. If there is no `1` anywhere, return `-1`.

### Examples

**Example 1**

Input:

```python
row_with_most_ones([[0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1]])
```

Output:

```text
1
```

Row 1 has three `1`s.

**Example 2**

Input:

```python
row_with_most_ones([[0, 0], [0, 0]])
```

Output:

```text
-1
```

There is no `1`.

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 2 * 10**5`
- Every row is sorted: zeros first, then ones.
- The big tests count how many cells you read.

## Explanation

Keep `col`, the start of the ones in the best row so far (`col = cols` means no ones yet). For every row, move `col` left while the cell just before it is a one; if it moved, this row has more ones than any earlier one, so remember it. A row that cannot move `col` costs one check.

`col` never moves right, so the total walk is at most `cols` steps plus one check per row: `O(r + c)`. Ties keep the earlier row because only a strictly longer run changes the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                                                |
| ---------------------------------- | -------------------------------------------------------- |
| `best_row = -1`                    | `best_row = -1`                                          |
| `for i, row in enumerate(matrix):` | `col = 4, i = 0, row = [0, 0, 1, 1]`                     |
| `col -= 1`                         | `col = 3, moved = False`                                 |
| `col -= 1`                         | `col = 2, moved = True`                                  |
| `moved = False`                    | `best_row = 0, i = 1, row = [0, 1, 1, 1], moved = False` |
| `moved = True`                     | `col = 1, moved = True`                                  |
| `for i, row in enumerate(matrix):` | `best_row = 1, i = 2, row = [0, 0, 0, 1]`                |
| `return`                           | `returned = 1`                                           |

### Complexity

- Time: O(r + c). One pointer walks left along the best row boundary and never moves back; each row costs one check plus the cells the pointer passes.
- Space: O(1). Two numbers.
