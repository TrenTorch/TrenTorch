---
name: sheet-check-sorted-rotated
title: 'Sorted, Maybe Rotated'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: counting-the-drops
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

## Explanation

Count `i` in `0..n-1` with `nums[i] > nums[(i + 1) % n]`. If the count is at most `1`, the answer is `True`.

For one value the single comparison is `nums[0] > nums[0]`, which is false, so the count is `0`. For equal values no comparison is true.

### Complexity

- Time: O(n). One pass counting the places where the order drops (wrapping around once).
- Space: O(1). One counter.
