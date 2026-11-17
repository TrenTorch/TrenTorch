---
name: sheet-upper-bound
title: 'Upper Bound'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Beginner
theory: upper-bound-first-value-larger
---

## Statement

`nums` is sorted in non-decreasing order and may contain repeated values. Return the **first index** `i` with `nums[i] > target`. If no value is greater, return `len(nums)`.

This is where `target` would be inserted to keep the list sorted, **after** any equal values.

### Examples

**Example 1**

Input:

```python
upper_bound([1, 2, 2, 2, 5], 2)
```

Output:

```text
4
```

The first value greater than 2 is `5` at index 4.

**Example 2**

Input:

```python
upper_bound([1, 3, 5], 0)
```

Output:

```text
0
```

Every value is greater than 0, so the answer is 0.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in non-decreasing order.
- `-10**9 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Explanation

The only difference from the lower bound is the comparison: a value `<= target` is not big enough, so `lo = mid + 1`; a value `> target` could be the answer, so `hi = mid`.

### Complexity

- Time: O(log n). The search range halves at every step.
- Space: O(1). Two indices.
