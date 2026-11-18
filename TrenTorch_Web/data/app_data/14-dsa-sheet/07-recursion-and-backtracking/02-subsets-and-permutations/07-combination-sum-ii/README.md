---
name: sheet-combination-sum-ii
title: 'Combination Sum, Each Number Once'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
theory: sums-where-each-item-is-used-once
---

## Statement

`candidates` are positive whole numbers that may repeat. Return every **different combination** that adds up to `target`, using **each position at most once**. Write each combination in increasing order and list them in dictionary order.

For `[10, 1, 2, 7, 6, 1, 5]` and `target = 8`: `[1, 1, 6]`, `[1, 2, 5]`, `[1, 7]`, `[2, 6]`.

### Examples

**Example 1**

Input:

```python
combination_sum_ii([10, 1, 2, 7, 6, 1, 5], 8)
```

Output:

```text
[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

**Example 2**

Input:

```python
combination_sum_ii([2, 5, 2, 1, 2], 5)
```

Output:

```text
[[1, 2, 2], [5]]
```

### Constraints

- `0 <= len(candidates) <= 14`
- `1 <= candidates[i] <= 30`
- `1 <= target <= 60`

## Explanation

Sort first so equal values are neighbours. In each loop, skip a value equal to the previous one at the same level, stop when a value exceeds the remainder, and recurse with `j + 1` so each position is used once.

### Complexity

- Time: O(2^n) worst case. Each candidate is either taken or not; sorting, the duplicate skip and the early `break` prune branches.
- Space: O(n). Recursion depth, plus the output.
