---
name: sheet-rotate-left
title: 'Rotate Left'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: slicing-and-zip
---

## Statement

Return a new list that is `nums` rotated to the left by `k` places: the first `k` elements move to the end, in order. `k` can be larger than the length of the list; rotating by the full length changes nothing.

### Examples

**Example 1**

Input:

```python
rotate_left([1, 2, 3, 4, 5], 2)
```

Output:

```text
[3, 4, 5, 1, 2]
```

The first two elements move to the back.

**Example 2**

Input:

```python
rotate_left([1, 2, 3], 7)
```

Output:

```text
[2, 3, 1]
```

Rotating by 7 is the same as rotating by 1.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= k <= 10**18`
- Do not change `nums`.

## Explanation

For an empty list return `[]`. Otherwise `k %= len(nums)` and return `nums[k:] + nums[:k]`.

Python slices never raise an error for out-of-range indices, so `k = 0` works without a special case.

### Complexity

- Time: O(n). Two slices and one concatenation copy each element a constant number of times.
- Space: O(n). A new list is required because `nums` must not change.
