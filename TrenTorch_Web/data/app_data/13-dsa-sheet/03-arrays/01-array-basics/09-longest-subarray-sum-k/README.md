---
name: sheet-longest-subarray-sum-k
title: 'Longest Subarray With Sum K'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Intermediate
---

## Statement

`nums` contains only values that are `0` or more. Return the length of the **longest contiguous run** of values that adds up to exactly `k`, or `0` if no run does.

A simple solution tries every start and end. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
longest_subarray_sum_k([1, 2, 3, 1, 1, 1, 1], 3)
```

Output:

```text
3
```

The run `[1, 1, 1]` and the run `[1, 2]` both add to 3, but `[1, 1, 1, 1]` has sum 4, so the longest with sum 3 has length 3.

**Example 2**

Input:

```python
longest_subarray_sum_k([2, 4, 6], 5)
```

Output:

```text
0
```

No run adds to 5.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**4`
- `0 <= k <= 10**9`

## Theory

Trying every start and end is `O(n²)`. Because no value is negative, adding a value to a run can only **increase** its sum, and removing a value from the front can only **decrease** it. That monotonic behaviour lets you use a **sliding window**.

Keep a window `[left, right]` and its sum. Move `right` forward and add the value. While the sum is too big, remove values from the left. When the sum equals `k`, record the window length. Each value enters and leaves the window at most once, so the total work is `O(n)`.

This only works for non-negative values. With negative values the sum is no longer monotonic, and you need prefix sums and a dictionary instead.

## Explanation

`total` is the sum of `nums[left..right]`. After adding `nums[right]`, shrink from the left while `total > k`. Then check `total == k` and update `best`. If `left` passes `right` the window is empty with sum `0`; recording its length `0` changes nothing.

`k = 0` works too: a run of zeros has sum `0`, and the window keeps all of them.
