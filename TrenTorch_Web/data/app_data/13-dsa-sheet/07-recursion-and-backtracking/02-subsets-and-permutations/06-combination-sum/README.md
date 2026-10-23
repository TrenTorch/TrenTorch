---
name: sheet-combination-sum
title: 'Combination Sum'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
---

## Statement

`candidates` are different positive whole numbers. Return every **different combination** of them that adds up to `target`, where **each candidate can be used any number of times**. Write each combination in increasing order, and list the combinations in dictionary order.

For `candidates = [2, 3, 6, 7]` and `target = 7`: `[2, 2, 3]` and `[7]`.

### Examples

**Example 1**

Input:

```python
combination_sum([2, 3, 6, 7], 7)
```

Output:

```text
[[2, 2, 3], [7]]
```

**Example 2**

Input:

```python
combination_sum([2], 1)
```

Output:

```text
[]
```

### Constraints

- `0 <= len(candidates) <= 8`
- `1 <= candidates[i] <= 30`, all different
- `1 <= target <= 40`

## Theory

At each step the recursion decides **which candidate to add next**, and a candidate may be used again, so the next call starts at the **same index** `j` (not `j + 1`). To avoid the same combination in different orders (`[2, 3]` and `[3, 2]`), only allow choices at or after the index you are at: that forces combinations to be written in increasing order.

**Prune** to stop early: sort the candidates, and when `a[j]` is bigger than what is left to reach the target, no later candidate can fit either, so `break`. When the remaining target is `0`, you have found a combination.

Pruning is the difference between backtracking and brute force: cut off any branch that cannot lead to an answer.

## Explanation

`go(i, remaining, current)` records `current` when `remaining == 0`. Otherwise it tries each candidate from index `i`; a candidate above `remaining` ends the loop (sorted, so the rest are bigger). Reusing a candidate is `go(j, ...)` with the same `j`.
