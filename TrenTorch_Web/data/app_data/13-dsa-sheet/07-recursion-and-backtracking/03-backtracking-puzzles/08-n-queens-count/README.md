---
name: sheet-n-queens-count
title: 'N Queens: Count the Solutions'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Advanced
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

## Theory

Place one queen per row, from the top. Row `r` needs a column that is not attacked: not in a column already used, and not on a diagonal of an earlier queen. **Backtracking**: try each column in row `r`; if it is safe place the queen and recurse to row `r + 1`; if you reach row `n` all queens are placed (count one); then remove the queen and try the next column.

To test "is this square attacked" in `O(1)`, keep **three sets**: used columns, used `r - c` values (one per `\` diagonal) and used `r + c` values (one per `/` diagonal). Squares on the same diagonal share `r - c` or `r + c`.

Compare with trying all `n^n` placements, or even all `n!` column permutations: pruning the moment two queens clash removes nearly all of them.

## Explanation

`go(r)` counts the solutions that extend the rows above `r`. For each column `c` that is not in `cols`, `r - c` is not in `diag1` and `r + c` is not in `diag2`, add the three markers, recurse, and remove them. Reaching `r == n` is one solution.
