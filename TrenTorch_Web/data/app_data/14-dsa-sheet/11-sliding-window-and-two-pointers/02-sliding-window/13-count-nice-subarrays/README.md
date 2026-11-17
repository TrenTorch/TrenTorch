---
name: sheet-count-nice-subarrays
title: 'Count Nice Subarrays'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: exactly-k-odd-numbers
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

## Explanation

The helper counts windows by their right end. Subtracting the two counts keeps exactly the subarrays whose odd count is `k`.

### Complexity

- Time: O(n). Two sliding-window passes: "at most k odd" minus "at most k - 1 odd".
- Space: O(1). A few numbers.
