---
name: sheet-subset-sum
title: 'Subset Sum'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
theory: subset-sum-and-its-cousins
---

## Statement

Return `True` if some **subset** of `nums` (possibly empty) adds up to exactly `target`.

For `nums = [3, 34, 4, 12, 5, 2]` and `target = 9` the answer is `True` (`4 + 5`).

The starter code tries taking or skipping every number. It is correct but too slow when there is no answer.

### Examples

**Example 1**

Input:

```python
subset_sum([3, 34, 4, 12, 5, 2], 9)
```

Output:

```text
True
```

**Example 2**

Input:

```python
subset_sum([3, 34, 4, 12, 5, 2], 30)
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 1000`
- `0 <= target <= 100000`

## Explanation

The shift by `x` adds `x` to every reachable sum at once, and the mask drops sums larger than the target.

### Complexity

- Time: O(n * T / w). `T` is the target and `w` the machine word size: each number shifts and ORs one big integer used as a bit set.
- Space: O(T / w). The bit set.
