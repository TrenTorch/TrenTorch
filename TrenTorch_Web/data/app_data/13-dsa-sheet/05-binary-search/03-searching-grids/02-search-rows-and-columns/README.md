---
name: sheet-search-rows-and-columns
title: 'Search a Row- and Column-Sorted Matrix'
tags: [dsa-sheet, binary-search, searching-grids]
difficulty: Advanced
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

**Explanation:** 5 is in the second row, so the function returns true.

**Example 2**

Input:

```python
search_matrix_ii([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 15)
```

Output:

```text
False
```

**Explanation:** 15 is not in the matrix, so the function returns false.

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 2 * 10**5`
- Every row and every column is sorted in increasing order.
- `-10**9 <= matrix[i][j], target <= 10**9`
- The big tests count how many cells you read.

## Theory

The flattened matrix is **not** sorted here, so the one-big-list trick fails. But you can still discard a whole row or column with each comparison if you start in the right corner.

Start at the **top-right** cell. It is the biggest value in its row and the smallest in its column. Compare it with the target: if it equals the target you are done. If it is **too big**, nothing below it in its column can help (they are even bigger), so move **left**. If it is **too small**, nothing to its left in its row can help (they are even smaller), so move **down**.

Each step removes a row or a column, so you take at most `rows + cols` steps: `O(rows + cols)`. It looks like a staircase walk toward the target.

## Explanation

`row, col` start at the top-right. While inside the matrix, compare `matrix[row][col]` with the target: equal returns `True`, bigger moves `col` left, smaller moves `row` down. Leaving the matrix means the target is absent.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables            |
| ---------------------------------- | -------------------- |
| `row, col = 0, len(matrix[0]) - 1` | `row = 0, col = 3`   |
| `value = matrix[row][col]`         | `value = 11`         |
| `col -= 1`                         | `col = 2`            |
| `value = matrix[row][col]`         | `value = 7`          |
| `value = matrix[row][col]`         | `col = 1, value = 4` |
| `row += 1`                         | `row = 1`            |
| `value = matrix[row][col]`         | `value = 5`          |
| `return`                           | `returned = True`    |

### Complexity

- Time: O(m + n), where m is the number of rows and n is the number of columns.
- Extra space: O(1), no extra memory is used.
- The brute force takes O(m * n), where m is the number of rows and n is the number of columns.
