---
name: sheet-subarrays-with-k-different-integers
title: 'Subarrays With K Different Values'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Mastery
theory: exactly-k-different-values
---

## Statement

Count the contiguous subarrays that contain **exactly `k` different values**.

For `nums = [1, 2, 1, 2, 3]` and `k = 2` the answer is `7`.

The starter code looks at every subarray. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
subarrays_k_distinct([1, 2, 1, 2, 3], 2)
```

Output:

```text
7
```

**Example 2**

Input:

```python
subarrays_k_distinct([1, 2, 1, 3, 4], 3)
```

Output:

```text
3
```

### Constraints

- `0 <= len(nums) <= 200000`
- `1 <= k <= len(nums)` (when the list is not empty)
- `1 <= nums[i] <= len(nums)`

## Explanation

`at_most(m)` slides a window keeping at most `m` different values and adds `right - left + 1` for every `right`. The difference removes the subarrays with fewer than `k` values.

### Complexity

- Time: O(n). Two sliding-window passes: "at most k" minus "at most k - 1".
- Space: O(k). The count map has at most `k + 1` entries.
