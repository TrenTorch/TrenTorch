---
name: sheet-maximal-square
title: 'Maximal Square'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `side(r, c)`, the side length of the largest all-ones square whose **bottom-right corner** is `(r, c)`. **Transition:** if the cell is `0`, `side = 0`. Otherwise the square is limited by its three neighbours up, left and up-left: `side(r, c) = 1 + min(side(r - 1, c), side(r, c - 1), side(r - 1, c - 1))`.

Why the minimum: a bigger square ending here needs all three smaller squares around it to be big enough. The answer is the square of the largest side seen. `O(rows × cols)`.

## Explanation

`prev` holds the previous row of sides and `cur` the row being built. The diagonal value is kept in `diag` since it is overwritten.
