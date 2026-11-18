---
name: sheet-squares-of-a-sorted-array
title: 'Squares of a Sorted Array'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Beginner
theory: squares-of-a-sorted-list
---

## Statement

`nums` is sorted in increasing order and may contain negative numbers. Return the **square of each number**, also sorted in increasing order, in `O(n)` time (sorting the squares works but takes `O(n log n)`).

For `[-4, -1, 0, 3, 10]` the answer is `[0, 1, 9, 16, 100]`.

### Examples

**Example 1**

Input:

```python
sorted_squares([-4, -1, 0, 3, 10])
```

Output:

```text
[0, 1, 9, 16, 100]
```

**Example 2**

Input:

```python
sorted_squares([-7, -3, 2, 3, 11])
```

Output:

```text
[4, 9, 9, 49, 121]
```

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**4 <= nums[i] <= 10**4`
- `nums` is sorted in increasing order.

## Explanation

`out[i]` is filled from the last index down. The pointer with the larger absolute value supplies the next square and moves inwards.

### Complexity

- Time: O(n). The largest square is at one of the two ends, so two pointers fill the result from the back.
- Space: O(n). The result list.
