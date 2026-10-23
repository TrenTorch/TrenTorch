---
name: sheet-count-nice-subarrays
title: 'Count Nice Subarrays'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Count the contiguous subarrays of `nums` that contain **exactly `k` odd numbers**.

For `nums = [1, 1, 2, 1, 1]` and `k = 3` the answer is `2`.

The starter code counts odd numbers in every subarray. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
number_of_subarrays([1, 1, 2, 1, 1], 3)
```

Output:

```text
2
```

**Example 2**

Input:

```python
number_of_subarrays([2, 4, 6], 1)
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= k <= len(nums)`
- `1 <= nums[i] <= 10**5`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Use the **exactly = at most minus at most one less** trick again: `at_most(k) - at_most(k - 1)`, where `at_most(m)` counts the subarrays with at most `m` odd numbers.

For `at_most(m)`: expand `right` (count it if odd), shrink `left` while the odd count exceeds `m`, and add `right - left + 1` for every `right`. For `m = -1` the answer is 0.

## Explanation

The helper counts windows by their right end. Subtracting the two counts keeps exactly the subarrays whose odd count is `k`.
