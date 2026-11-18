---
name: sheet-minimum-subset-sum-difference
title: 'Minimum Subset Sum Difference'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Advanced
theory: subset-sum-and-its-cousins
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

## Explanation

`bits` has bit `s` set when a subset sums to `s`. The loop from `total // 2` down finds the reachable sum closest to half.

### Complexity

- Time: O(n * S / w + S). `S` is the total sum: a bit set of reachable sums is built in `n` shifts, then scanned downward from `S / 2`.
- Space: O(S / w). The bit set.
