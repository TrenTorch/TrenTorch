---
name: sheet-rotation-count
title: 'How Many Times Was It Rotated?'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
theory: how-many-rotations
---

## Statement

A sorted list with **no repeated values** was rotated to the left by some amount (for example `[1, 2, 3, 4, 5]` rotated left by 2 is `[3, 4, 5, 1, 2]`). Return that amount, a number from `0` to `len(nums) - 1`.

### Examples

**Example 1**

Input:

```python
rotation_count([3, 4, 5, 1, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
rotation_count([1, 2, 3])
```

Output:

```text
0
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- All values are different; the list is a sorted list rotated left.
- `-10**9 <= nums[i] <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Explanation

The same search as the rotated minimum: compare `nums[mid]` with `nums[hi]`, move `lo` or `hi`, and stop when `lo == hi`. That index is where the smallest value sits, which equals the number of left rotations.

### Complexity

- Time: O(log n). The rotation count is the index of the minimum, found by the same halving search.
- Space: O(1). Two indices.
