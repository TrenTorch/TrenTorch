---
name: sheet-max-sum-subarray-of-size-k
title: 'Maximum Sum of K Consecutive Values'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Beginner
theory: the-best-block-of-k-values
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

**Example 2**

Input:

```python
max_sum_k([2, 3, 4, 1, 5], 2)
```

Output:

```text
7
```

### Constraints

- `1 <= k <= len(nums) <= 200000`
- `-10**4 <= nums[i] <= 10**4`

## Explanation

`total` is the sum of the current window. Adding the new value and subtracting the one that left gives the next window's sum.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables          |
| ---------------------------------------- | ------------------ |
| `total = sum(nums[i] for i in range(k))` | `total = 8`        |
| `best = total`                           | `best = 8`         |
| `total += nums[i] - nums[i - k]`         | `total = 7, i = 3` |
| `for i in range(k, len(nums)):`          | `i = 4`            |
| `total += nums[i] - nums[i - k]`         | `total = 9`        |
| `best = max(best, total)`                | `best = 9`         |
| `total += nums[i] - nums[i - k]`         | `total = 6, i = 5` |
| `return`                                 | `returned = 9`     |

### Complexity

- Time: O(n). The window sum is updated by adding one value and removing one.
- Space: O(1). A few numbers.
