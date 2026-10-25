---
name: sheet-max-sum-subarray-of-size-k
title: 'Maximum Sum of K Consecutive Values'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Beginner
---

## Statement

Return the **largest sum of `k` consecutive values** in `nums`.

For `nums = [2, 1, 5, 1, 3, 2]` and `k = 3` the answer is `9` (`5 + 1 + 3`).

The starter code adds up every window from scratch. It is correct but too slow when `k` is large.

### Examples

**Example 1**

Input:

```python
max_sum_k([2, 1, 5, 1, 3, 2], 3)
```

Output:

```text
9
```

**Explanation:** The subarrays of length 3 are [2, 1, 5] (sum 8), [1, 5, 1] (sum 7), [5, 1, 3] (sum 9), and [1, 3, 2] (sum 6). The maximum sum is 9.

**Example 2**

Input:

```python
max_sum_k([2, 3, 4, 1, 5], 2)
```

Output:

```text
7
```

**Explanation:** The subarrays of length 2 are [2, 3] (sum 5), [3, 4] (sum 7), [4, 1] (sum 5), and [1, 5] (sum 6). The maximum sum is 7.

### Constraints

- `1 <= k <= len(nums) <= 200000`
- `-10**4 <= nums[i] <= 10**4`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Here the window has a **fixed size** `k`. When it slides one step, only two values change: the new value on the right enters and the old value on the left leaves. So instead of adding `k` numbers again, update the sum: `window_sum += nums[right] - nums[right - k]`.

Compute the first window directly, then slide. Each step is `O(1)`, so the whole pass is `O(n)` instead of `O(n * k)`.

## Explanation

`total` is the sum of the current window. Adding the new value and subtracting the one that left gives the next window's sum.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables          |
| -------------------------------- | ------------------ |
| `total = sum(nums[:k])`          | `total = 8`        |
| `best = total`                   | `best = 8`         |
| `total += nums[i] - nums[i - k]` | `total = 7, i = 3` |
| `for i in range(k, len(nums)):`  | `i = 4`            |
| `total += nums[i] - nums[i - k]` | `total = 9`        |
| `best = max(best, total)`        | `best = 9`         |
| `total += nums[i] - nums[i - k]` | `total = 6, i = 5` |
| `return`                         | `returned = 9`     |

### Complexity

- Time: O(n + k) where n=nums length, k=window size.
- Extra space: O(1).
- The brute force takes O(n * k).
