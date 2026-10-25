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

**Explanation:** The longest subarray that fits the limit is [2,4], giving length 2.

**Example 2**

Input:

```python
longest_within_limit([10, 1, 2, 4, 7, 2], 5)
```

Output:

```text
4
```

**Explanation:** A subarray like [2,4,7,2] has max 7 min 2 diff 5 equal to the limit, length 4, and no longer subarray satisfies the limit.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                                                   |
| ------------------------------------ | ----------------------------------------------------------- |
| `big = deque()`                      | `big = deque([])`                                           |
| `for right, x in enumerate(nums):`   | `small = deque([]), left = 0, best = 0, right = 0, x = 8`   |
| `best = max(best, right - left + 1)` | `big = deque([0]), small = deque([0]), best = 1`            |
| `small.append(right)`                | `big = deque([0, 1]), small = deque([1]), right = 1, x = 2` |
| `for right, x in enumerate(nums):`   | `big = deque([1]), left = 1, right = 2, x = 4`              |
| `best = max(best, right - left + 1)` | `big = deque([2]), small = deque([1, 2]), best = 2`         |
| `big.append(right)`                  | `big = deque([3]), right = 3, x = 7`                        |
| `return`                             | `returned = 2`                                              |

### Complexity

- Time: O(n) array length.
- Extra space: O(n) array length.
- The brute force takes O(n^2) array length.
