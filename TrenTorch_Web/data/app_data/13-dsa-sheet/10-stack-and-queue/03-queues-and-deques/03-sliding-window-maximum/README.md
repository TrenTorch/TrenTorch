---
name: sheet-sliding-window-maximum
title: 'Sliding Window Maximum'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Advanced
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

**Explanation:** For the first window [1,3,-1] the maximum is 3; sliding the window step by step gives maxes 3, 3, 5, 5, 6, 7.

**Example 2**

Input:

```python
sliding_window_max([1], 1)
```

Output:

```text
[1]
```

**Explanation:** Only one element, so the maximum in the only window is 1.

### Constraints

- `1 <= k <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Scanning each window costs `O(n * k)`. A **monotonic deque** (double-ended queue, `collections.deque`) gives `O(n)`.

Keep a deque of **indices** whose values decrease from front to back. The **front** is always the index of the current window's maximum. For each new element `i`:

1. **Remove from the back** all indices whose value is `<= nums[i]`: they can never be a maximum again, since `nums[i]` is bigger and stays in the window longer.
2. Add `i` at the back.
3. If the front index has left the window (`front <= i - k`), remove it from the front.
4. Once `i >= k - 1`, the front holds the answer for this window.

Every index is added once and removed once: `O(n)`.

## Explanation

The deque is a stack at the back (for the monotonic order) and a queue at the front (for expiring old indices). Both ends of a `deque` are `O(1)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                                  |
| ------------------------------ | ---------------------------------------------------------- |
| `window = deque()`             | `window = deque([])`                                       |
| `for i, x in enumerate(nums):` | `window = deque([0]), out = [], i = 1, x = 3`              |
| `out.append(nums[window[0]])`  | `window = deque([1, 2]), out = [3], i = 2, x = -1`         |
| `for i, x in enumerate(nums):` | `window = deque([1, 2, 3]), out = [3, 3], i = 4, x = 5`    |
| `out.append(nums[window[0]])`  | `window = deque([4]), out = [3, 3, 5]`                     |
| `for i, x in enumerate(nums):` | `window = deque([4, 5]), out = [3, 3, 5, 5], i = 6, x = 6` |
| `for i, x in enumerate(nums):` | `window = deque([6]), out = [3, 3, 5, 5, 6], i = 7, x = 7` |
| `return`                       | `returned = [3, 3, 5, 5, 6, 7]`                            |

### Complexity

- Time: O(n), n is length of nums.
- Extra space: O(k), k is window size.
- The brute force takes O(nk), n is length, k is window size.
