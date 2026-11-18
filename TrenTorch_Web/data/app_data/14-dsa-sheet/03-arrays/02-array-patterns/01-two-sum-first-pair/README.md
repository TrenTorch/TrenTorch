---
name: sheet-two-sum-first-pair
title: 'Two Sum: First Pair'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Beginner
theory: looking-back-for-a-partner
---

## Statement

Find two **different positions** `i < j` with `nums[i] + nums[j] == target` and return `[i, j]`.

If several pairs work, return the one with the **smallest `i`**, and among those the smallest `j`. If no pair works, return `[-1, -1]`.

The starter code checks every pair. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
two_sum_first_pair([1, 6, 5, 3, 8], 9)
```

Output:

```text
[0, 4]
```

`1 + 8` (positions 0 and 4) and `6 + 3` (positions 1 and 3) both work. The first has the smaller `i`.

**Example 2**

Input:

```python
two_sum_first_pair([2, 4], 7)
```

Output:

```text
[-1, -1]
```

No pair adds to 7.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`
- `-1 <= target <= 2 * 10**9`

## Explanation

`first[v]` is the first index of value `v`. For each `j`, if `target - nums[j]` has a first index `i < j`, then `(i, j)` is a candidate. The best candidate is the smallest tuple. The scan covers every `j`, so it cannot miss a pair with a smaller `i` found later.

### Complexity

- Time: O(n). One pass with one dictionary lookup per element (O(1) on average).
- Space: O(n). The dictionary of first positions.
