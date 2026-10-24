---
name: sheet-has-duplicate
title: 'Has Duplicate'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Beginner
---

## Statement

Given a list of integers `nums`, return `True` if some value appears at least twice, and `False` if every value is different.

The starter code is correct, but it compares every pair of values, which is too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
has_duplicate([1, 2, 3, 1])
```

Output:

```text
True
```

**Example 2**

Input:

```python
has_duplicate([1, 2, 3, 4])
```

Output:

```text
False
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Comparing every pair is `O(n²)`: `2 * 10⁵` numbers means about `2 * 10¹⁰` comparisons, far too many for one second.

The fix is a trade of memory for time. A `set` answers "have I seen this value?" in `O(1)` on average, because it stores values by a hash (a number computed from the value that tells where to look). Walk the list once, and stop at the first value already in the set. That is `O(n)` time and `O(n)` extra memory.

## Explanation

Keep a set of values seen so far. For each value, if it is already in the set the answer is `True`; otherwise add it. If the loop ends, every value was new.

A shorter version compares sizes: `len(set(nums)) != len(nums)`. It does the same work, but it always builds the whole set even when the first two values are equal.
