---
name: sheet-minimum-subset-sum-difference
title: 'Minimum Subset Sum Difference'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Advanced
---

## Statement

Split `nums` into **two groups** (every number goes into exactly one; a group may be empty). Return the **smallest possible difference** between the two sums.

For `[1, 6, 11, 5]` the answer is `1` (`1 + 5 + 6 = 12` and `11`).

### Examples

**Example 1**

Input:

```python
min_subset_difference([1, 6, 11, 5])
```

Output:

```text
1
```

**Example 2**

Input:

```python
min_subset_difference([3, 9, 7, 3])
```

Output:

```text
2
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

If one group has sum `s`, the other has `total - s` and the difference is `|total - 2s|`. So you want the reachable subset sum `s` that is **closest to `total / 2`**. That is the subset sum table: compute every reachable `s` up to `total` (a bitset again), then take the best `s <= total / 2`.

The answer is `total - 2 × (largest reachable s not above total / 2)`. `O(n × total / 64)`.

## Explanation

`bits` has bit `s` set when a subset sums to `s`. The loop from `total // 2` down finds the reachable sum closest to half.
