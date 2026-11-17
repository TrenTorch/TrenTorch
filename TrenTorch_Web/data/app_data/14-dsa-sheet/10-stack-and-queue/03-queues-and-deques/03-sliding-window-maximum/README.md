---
name: sheet-sliding-window-maximum
title: 'Sliding Window Maximum'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
theory: sliding-window-maximum
---

## Statement

A window of size `k` slides from the left end of `nums` to the right end, one position at a time. Return the **maximum value in each window position**: a list of `len(nums) - k + 1` values.

For `nums = [1, 3, -1, -3, 5, 3, 6, 7]` and `k = 3` the answer is `[3, 3, 5, 5, 6, 7]`.

The starter code scans every window. It is correct but too slow when `k` is large.

### Examples

**Example 1**

Input:

```python
sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
```

Output:

```text
[3, 3, 5, 5, 6, 7]
```

**Example 2**

Input:

```python
sliding_window_max([1], 1)
```

Output:

```text
[1]
```

### Constraints

- `1 <= k <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

The deque is a stack at the back (for the monotonic order) and a queue at the front (for expiring old indices). Both ends of a `deque` are `O(1)`.

### Complexity

- Time: O(n). Each index enters and leaves the deque at most once.
- Space: O(k). The deque holds at most `k` indices (plus the result).
