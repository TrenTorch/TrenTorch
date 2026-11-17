---
name: sheet-three-sum-closest
title: 'Three Sum Closest'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: three-numbers-closest-sum
---

## Statement

Choose **three different positions** of `nums` and return the **sum that is closest to `target`**. If two sums are equally close, return the **smaller** one.

For `nums = [-1, 2, 1, -4]` and `target = 1` the answer is `2` (`-1 + 2 + 1`).

The starter code tries every triple. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
three_sum_closest([-1, 2, 1, -4], 1)
```

Output:

```text
2
```

**Example 2**

Input:

```python
three_sum_closest([0, 0, 0], 1)
```

Output:

```text
0
```

### Constraints

- `3 <= len(nums) <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-3000 <= target <= 3000`

## Explanation

Ties go to the smaller sum with the key `(abs(s - target), s)`. Each pointer pass moves `lo` or `hi` until they meet.

### Complexity

- Time: O(n^2). Sort once, then fix one value and sweep two pointers over the rest.
- Space: O(n). The sorted copy.
