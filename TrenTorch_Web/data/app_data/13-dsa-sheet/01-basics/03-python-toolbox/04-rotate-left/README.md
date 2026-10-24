---
name: sheet-rotate-left
title: 'Rotate Left'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
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

- `0 <= len(nums) <= 10**6`
- `0 <= k <= 10**18`
- Do not change `nums`.

## Theory

Slicing copies part of a list: `nums[k:]` is everything from index `k`, and `nums[:k]` is everything before it. Rotating left by `k` is `nums[k:] + nums[:k]`, in `O(n)`.

Rotating by `n` is the identity, so only `k % n` matters. Take the remainder first; this also keeps `k = 10**18` from doing anything silly. Check for an empty list before the `%`, because `k % 0` is an error.

For repeated rotations at both ends, `collections.deque` has `rotate(-k)`, which is the tool to reach for when you rotate a queue many times.

## Explanation

For an empty list return `[]`. Otherwise `k %= len(nums)` and return `nums[k:] + nums[:k]`.

Python slices never raise an error for out-of-range indices, so `k = 0` works without a special case.
