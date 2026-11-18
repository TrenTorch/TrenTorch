---
name: sheet-longest-subarray-sum-k
title: 'Longest Subarray With Sum K'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Intermediate
theory: a-window-that-grows-and-shrinks
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

## Explanation

`total` is the sum of `nums[left..right]`. After adding `nums[right]`, shrink from the left while `total > k`. Then check `total == k` and update `best`. If `left` passes `right` the window is empty with sum `0`; recording its length `0` changes nothing.

`k = 0` works too: a run of zeros has sum `0`, and the window keeps all of them.

### Complexity

- Time: O(n). Values are non-negative, so a sliding window works and each pointer only moves forward.
- Space: O(1). Two pointers and a running sum.
