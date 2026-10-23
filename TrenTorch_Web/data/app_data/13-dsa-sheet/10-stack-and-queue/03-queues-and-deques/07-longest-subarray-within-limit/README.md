---
name: sheet-longest-subarray-within-limit
title: 'Longest Subarray Within a Limit'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
---

## Statement

Return the **length of the longest contiguous subarray** in which the difference between the largest and the smallest value is **at most `limit`**.

For `nums = [8, 2, 4, 7]` and `limit = 4` the answer is `2` (the subarray `[2, 4]`).

The starter code recomputes the largest and smallest value of the window at every step. It is correct but too slow for long arrays.

### Examples

**Example 1**

Input:

```python
longest_within_limit([8, 2, 4, 7], 4)
```

Output:

```text
2
```

**Example 2**

Input:

```python
longest_within_limit([10, 1, 2, 4, 7, 2], 5)
```

Output:

```text
4
```

### Constraints

- `0 <= len(nums) <= 100000`
- `1 <= nums[i] <= 10**9`
- `0 <= limit <= 10**9`

## Theory

This is a sliding window (`left`, `right`) where the window is valid while `max - min <= limit`. Growing the window can only break validity, so when it breaks, advance `left` until it is valid again.

The hard part is knowing the window's **max and min quickly** as it slides. Use **two monotonic deques**, exactly as in the sliding window maximum: one keeps indices with decreasing values (front = max), the other indices with increasing values (front = min). When `left` moves past a front index, drop it.

Both deques make `max` and `min` `O(1)`, so the whole algorithm is `O(n)`.

## Explanation

`big` and `small` are the deques for the window's maximum and minimum. While the difference is above the limit, `left` moves right and the deques drop indices that fall out of the window.
