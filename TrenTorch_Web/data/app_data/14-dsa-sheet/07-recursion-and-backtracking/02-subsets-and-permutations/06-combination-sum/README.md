---
name: sheet-combination-sum
title: 'Combination Sum'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
theory: sums-where-items-repeat
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

## Explanation

`go(i, remaining, current)` records `current` when `remaining == 0`. Otherwise it tries each candidate from index `i`; a candidate above `remaining` ends the loop (sorted, so the rest are bigger). Reusing a candidate is `go(j, ...)` with the same `j`.

### Complexity

- Time: O(n^(T/m)) worst case. The recursion is at most `T / m` deep (`T` = target, `m` = smallest candidate) with up to `n` choices per level; sorting and the early `break` prune most branches.
- Space: O(T / m). Recursion depth, plus the output.
