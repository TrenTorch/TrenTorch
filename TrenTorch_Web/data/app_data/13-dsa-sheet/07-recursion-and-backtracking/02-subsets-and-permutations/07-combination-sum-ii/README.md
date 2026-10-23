---
name: sheet-combination-sum-ii
title: 'Combination Sum, Each Number Once'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
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

## Theory

This mixes two ideas you already have. Each number can be used **once**, so recurse with `j + 1` (as in subsets). The input may contain **duplicates**, so skip an equal value at the same level (`j > start and a[j] == a[j - 1]`), as in subsets with duplicates. And **prune** with the sorted order: once `a[j]` is bigger than the remainder, stop the loop.

When you meet a new problem in this family, ask three questions: _can a value be reused?_ (same index or next index), _can the input repeat?_ (skip equal values at the same level), and _can I cut a branch early?_ (pruning).

## Explanation

Sort first so equal values are neighbours. In each loop, skip a value equal to the previous one at the same level, stop when a value exceeds the remainder, and recurse with `j + 1` so each position is used once.
