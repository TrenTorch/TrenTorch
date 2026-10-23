---
name: sheet-check-sorted-rotated
title: 'Sorted, Maybe Rotated'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

Return `True` if `nums` is **sorted in non-decreasing order, possibly after rotating it**. A rotation moves some values from the front to the back without changing their order, so `[3, 4, 5, 1, 2]` is the sorted list `[1, 2, 3, 4, 5]` rotated. A list that is already sorted counts, and so does a list of equal values.

### Examples

**Example 1**

Input:

```python
check_sorted_rotated([3, 4, 5, 1, 2])
```

Output:

```text
True
```

It is `[1, 2, 3, 4, 5]` rotated by 2.

**Example 2**

Input:

```python
check_sorted_rotated([2, 1, 3, 4])
```

Output:

```text
False
```

It drops twice (2 to 1, and 4 back to 2).

### Constraints

- `1 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

You could try every rotation and test whether it is sorted, but that is `O(n²)`. Think about what a rotated sorted list looks like when you walk around it as a **circle**: it climbs, and there is exactly one place where it drops from the biggest value back to the smallest.

So count the **drops**: positions `i` where `nums[i] > nums[i + 1]`, treating the list as circular (the last value is followed by the first). A sorted list has no drop. A rotated sorted list has exactly one. Anything with two or more drops cannot be fixed by a rotation.

The index trick `(i + 1) % n` wraps the last position back to `0`, and it is the standard way to walk a circular array.

## Explanation

Count `i` in `0..n-1` with `nums[i] > nums[(i + 1) % n]`. If the count is at most `1`, the answer is `True`.

For one value the single comparison is `nums[0] > nums[0]`, which is false, so the count is `0`. For equal values no comparison is true.
