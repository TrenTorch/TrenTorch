---
name: sheet-longest-subarray-within-limit
title: 'Longest Subarray Within a Limit'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
theory: a-window-that-grows-and-shrinks
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

## Explanation

`big` and `small` are the deques for the window's maximum and minimum. While the difference is above the limit, `left` moves right and the deques drop indices that fall out of the window.

### Complexity

- Time: O(n). Two monotonic deques give the window maximum and minimum in O(1); each index enters and leaves each deque once.
- Space: O(n). The two deques can hold the whole window.
