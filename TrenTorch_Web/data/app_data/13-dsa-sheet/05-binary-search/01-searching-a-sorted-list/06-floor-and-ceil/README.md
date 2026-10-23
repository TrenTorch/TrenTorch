---
name: sheet-floor-and-ceil
title: 'Floor and Ceil'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
---

## Statement

`nums` is sorted in non-decreasing order. For a `target`, the **floor** is the largest value in `nums` that is `<= target`, and the **ceil** is the smallest value that is `>= target`. Return `[floor, ceil]`, using `-1` for one that does not exist.

### Examples

**Example 1**

Input:

```python
floor_and_ceil([1, 2, 8, 10, 11, 12, 19], 5)
```

Output:

```text
[2, 8]
```

The floor is 2 and the ceil is 8.

**Example 2**

Input:

```python
floor_and_ceil([3, 4], 1)
```

Output:

```text
[-1, 3]
```

Nothing is `<= 1`, so the floor is -1. The ceil is 3.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in non-decreasing order.
- `0 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

Both answers sit next to the place where the target would be inserted. Find `i = lower_bound(target)`, the first index with `nums[i] >= target`.

The **ceil** is `nums[i]` if `i` is inside the list, otherwise it does not exist. The **floor** is `target` itself when `nums[i] == target`; otherwise it is the value just before the insertion point, `nums[i - 1]`, if there is one.

One binary search plus two extra reads: `O(log n)`.

## Explanation

`i` is the lower bound. If `i < n`, `nums[i]` is the ceil, and when it equals the target it is also the floor. Otherwise the floor is `nums[i - 1]` when `i > 0`. Missing values are reported as `-1`; the constraints keep real values non-negative so `-1` is unambiguous.
