---
name: sheet-max-subarray-sum
title: 'Maximum Subarray Sum'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
theory: best-sum-ending-here
---

## Statement

Given a non-empty list of integers `nums`, return the largest sum of a **contiguous** run of one or more elements (a subarray).

The starter code tries every start and end. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
```

Output:

```text
6
```

The best run is `[4, -1, 2, 1]` with sum 6.

**Example 2**

Input:

```python
max_subarray_sum([-3, -1, -2])
```

Output:

```text
-1
```

All values are negative, so the best run is the single element `-1`.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`
- The subarray must contain at least one element.

## Explanation

`cur` is the best sum of a subarray that ends at the current element. Extending is `cur + x`; starting fresh is `x`. Take the larger, and keep the overall maximum in `best`.

Start from the first element (not `0`), so a list of all negative numbers returns its largest single element and not `0`.

### Complexity

- Time: O(n). One pass; Kadane keeps the best sum ending here and the best sum seen so far.
- Space: O(1). Two running numbers.
