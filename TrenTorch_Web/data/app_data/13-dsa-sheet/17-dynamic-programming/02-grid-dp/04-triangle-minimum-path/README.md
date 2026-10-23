---
name: sheet-triangle-minimum-path
title: 'Triangle Minimum Path'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
---

## Statement

`triangle` has `i + 1` numbers in row `i`. Start at the top and move down; from position `j` of a row you may go to position `j` or `j + 1` of the next row. Return the **smallest sum** of a path from the top to the bottom. An empty triangle gives `0`.

For `[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]` the answer is `11` (`2 + 3 + 5 + 1`).

### Examples

**Example 1**

Input:

```python
minimum_total([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]])
```

Output:

```text
11
```

**Example 2**

Input:

```python
minimum_total([[-10]])
```

Output:

```text
-10
```

### Constraints

- `0 <= rows <= 1000`
- `-10**4 <= value <= 10**4`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Going **top-down** you have to remember a whole row of sums. A neat alternative is **bottom-up**: start with the last row as the answers for "starting at each bottom cell"; then for each higher row, `best[j] = value + min(best[j], best[j + 1])` (the better of the two cells below). The answer ends in `best[0]`.

Only one row is needed: update it in place, and it needs just `O(rows)` extra memory. The total time is `O(number of cells)`.

## Explanation

`best` starts as a copy of the last row. Each higher row replaces `best` with the cheapest total from each of its cells down to the bottom.
