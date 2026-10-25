---
name: sheet-spiral-order
title: 'Spiral Order'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
---

## Statement

Return all the values of the matrix in **clockwise spiral order**: along the top row left to right, down the right column, along the bottom row right to left, up the left column, then repeat on the inner part until every value is used.

### Examples

**Example 1**

Input:

```python
spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
```

Output:

```text
[1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**Explanation:** Traversing the outer boundary yields 1, 2, 3 going right, 6, 9 going down, 8, 7 going left, and 4 going up, leaving the inner element 5 to complete the spiral.

**Example 2**

Input:

```python
spiral_order([[1, 2, 3, 4]])
```

Output:

```text
[1, 2, 3, 4]
```

**Explanation:** With only a single row, the traversal simply moves from left to right along that row to visit 1, 2, 3, and 4.

### Constraints

- `0 <= rows, cols`, and `rows * cols <= 250000`
- All rows have the same length.

## Theory

The spiral peels the matrix like an onion, one **layer** at a time. Keep four boundaries: `top`, `bottom`, `left`, `right`. Walk the top row, then shrink `top`; walk the right column, then shrink `right`; walk the bottom row, then shrink `bottom`; walk the left column, then shrink `left`. Repeat while the boundaries have not crossed.

The easy bug is the last layer. When it is a single row or a single column, the "bottom row" or "left column" walk would revisit cells. That is why you must check that `top <= bottom` and `left <= right` again **before** the third and fourth walks.

Each cell is visited exactly once: `O(rows * cols)`.

## Explanation

The loop `while top <= bottom and left <= right` handles one layer. After walking the top row and the right column, the bottom row is walked only if `top <= bottom` still holds, and the left column only if `left <= right` still holds. These checks stop a single row or column from being walked twice.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                             | Variables                                                   |
| ------------------------------------------- | ----------------------------------------------------------- |
| `out = []`                                  | `out = []`                                                  |
| `out.extend(matrix[top][left : right + 1])` | `out = [1, 2, 3], top = 0, bottom = 2, left = 0, right = 2` |
| `for i in range(top + 1, bottom + 1):`      | `out = [1, 2, 3, 6], i = 2`                                 |
| `for i in range(bottom - 1, top, -1):`      | `out = [1, 2, 3, 6, 9, 8, 7], i = 1`                        |
| `top += 1`                                  | `out = [1, 2, 3, 6, 9, 8, 7, 4], top = 1`                   |
| `right -= 1`                                | `bottom = 1, left = 1, right = 1`                           |
| `bottom -= 1`                               | `out = [1, 2, 3, 6, 9, 8, 7, 4, 5], top = 2, bottom = 0`    |
| `return`                                    | `returned = [1, 2, 3, 6, 9, 8, 7, 4, 5]`                    |

### Complexity

- Time: O(n * q), where n is the number of rows and q is the number of columns.
- Extra space: O(1), no extra memory is used.
- The brute force takes O(n * q), where n is the number of rows and q is the number of columns.
