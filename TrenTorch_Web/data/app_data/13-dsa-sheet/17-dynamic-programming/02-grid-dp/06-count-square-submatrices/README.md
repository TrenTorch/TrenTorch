---
name: sheet-count-square-submatrices
title: 'Count Square Submatrices of Ones'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
---

## Statement

`matrix` holds `0`s and `1`s. Return the **number of square submatrices** (of any size) that contain only `1`s.

For `[[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]` the answer is `15`.

### Examples

**Example 1**

Input:

```python
count_squares([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]])
```

Output:

```text
15
```

**Explanation:** Each 1 contributes squares equal to the size of the largest all-ones square ending there; summing gives 15 for the 3x4 matrix.

**Example 2**

Input:

```python
count_squares([[1, 0, 1], [1, 1, 0], [1, 1, 0]])
```

Output:

```text
7
```

**Explanation:** Similarly, for the 3x3 matrix, contributing squares from each 1 give a total of 7.

### Constraints

- `0 <= rows, cols <= 500`
- Every cell is `0` or `1`.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Use the same table as the maximal square question: `side(r, c)` is the largest all-ones square with its bottom-right corner at `(r, c)`. The key observation: if the largest such square has side `k`, then there are exactly `k` all-ones squares with that bottom-right corner (of sides `1, 2, ..., k`).

So the answer is the **sum of `side(r, c)` over all cells**. `O(rows × cols)`.

## Explanation

The same DP as maximal square, but each cell adds its `side` to the total instead of updating a maximum.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                      | Variables                                                                          |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `rows = len(matrix)`                                 | `rows = 3`                                                                         |
| `for c in range(cols):`                              | `cols = 4, prev = [0, 0, 0, 0, 0], total = 0, r = 0, cur = [0, 0, 0, 0, 0], c = 0` |
| `for c in range(cols):`                              | `total = 2, cur = [0, 0, 1, 1, 0], c = 3`                                          |
| `for c in range(cols):`                              | `prev = [0, 0, 1, 1, 1], total = 3, r = 1, cur = [0, 0, 0, 0, 0], c = 0`           |
| `cur[c + 1] = 1 + min(prev[c], prev[c + 1], cur[c])` | `total = 5, cur = [0, 1, 1, 2, 0], c = 2`                                          |
| `for r in range(rows):`                              | `prev = [0, 1, 1, 2, 2], total = 9, r = 2, cur = [0, 1, 1, 2, 2], c = 3`           |
| `cur[c + 1] = 1 + min(prev[c], prev[c + 1], cur[c])` | `total = 10, cur = [0, 0, 1, 2, 0], c = 2`                                         |
| `return`                                             | `returned = 15`                                                                    |

### Complexity

- Time: O(n * m), where n is the number of rows and m is the number of columns.
- Extra space: O(m), where m is the number of columns.
- The brute force takes O(n^3 * m^3), where n is the number of rows and m is the number of columns.
