---
name: sheet-n-queens-count
title: 'N Queens: Count the Solutions'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Advanced
theory: queens-that-do-not-attack
---

## Statement

Place `n` chess queens on an `n x n` board so that **no two queens attack each other**: no two share a row, a column or a diagonal. Return **how many different ways** there are.

For `n = 4` there are 2. For `n = 1` there is 1, and for `n = 2` and `n = 3` there are none.

### Examples

**Example 1**

Input:

```python
n_queens_count(4)
```

Output:

```text
2
```

**Example 2**

Input:

```python
n_queens_count(1)
```

Output:

```text
1
```

### Constraints

- `0 <= n <= 9`

## Explanation

`go(r)` counts the solutions that extend the rows above `r`. For each column `c` that is not in `cols`, `r - c` is not in `diag1` and `r + c` is not in `diag2`, add the three markers, recurse, and remove them. Reaching `r == n` is one solution.

### Complexity

- Time: O(n!). One queen per row with columns and both diagonals blocked, so at most `n!` placements are explored.
- Space: O(n). The three sets and the recursion.
