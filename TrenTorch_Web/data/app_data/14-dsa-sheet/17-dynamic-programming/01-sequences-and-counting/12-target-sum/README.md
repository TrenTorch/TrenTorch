---
name: sheet-target-sum
title: 'Target Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: counting-versions-and-two-budgets
---

## Statement

Put a `+` or a `-` in front of **every** number of `nums`. Return the **number of ways** to make the total equal `target`.

For `nums = [1, 1, 1, 1, 1]` and `target = 3` the answer is `5`.

### Examples

**Example 1**

Input:

```python
find_target_sum_ways([1, 1, 1, 1, 1], 3)
```

Output:

```text
5
```

**Example 2**

Input:

```python
find_target_sum_ways([1], 1)
```

Output:

```text
1
```

### Constraints

- `0 <= len(nums) <= 100`
- `0 <= nums[i] <= 100`
- `-10**4 <= target <= 10**4`

## Explanation

`ways` maps each reachable sum to the number of sign choices that give it. The final answer is the count stored for `target`.

### Complexity

- Time: O(n * S). `S` is the number of different sums reachable (at most the total of the numbers): for each number every known sum is extended in two ways.
- Space: O(S). The table of counts per sum.
