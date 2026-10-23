---
name: sheet-subarrays-with-k-different-integers
title: 'Subarrays With K Different Values'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Mastery
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

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

"Exactly `k`" is awkward for a window, because shrinking and growing can move in and out of exactly `k`. The standard trick: **exactly `k` = at most `k` minus at most `k - 1`**.

"At most `k` distinct" is the easy version. For each `right`, the windows ending at `right` that have at most `k` distinct values start at any position from the smallest valid `left` up to `right`: that is `right - left + 1` subarrays. Sum that over all `right`.

So the answer is `at_most(k) - at_most(k - 1)`. Two passes of `O(n)`.

## Explanation

`at_most(m)` slides a window keeping at most `m` different values and adds `right - left + 1` for every `right`. The difference removes the subarrays with fewer than `k` values.
