---
name: sheet-has-duplicate
title: 'Has Duplicate'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Beginner
theory: a-set-that-answers-seen-it-instantly
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

## Explanation

Keep a set of values seen so far. For each value, if it is already in the set the answer is `True`; otherwise add it. If the loop ends, every value was new.

A shorter version compares sizes: `len(set(nums)) != len(nums)`. It does the same work, but it always builds the whole set even when the first two values are equal.

### Complexity

- Time: O(n). Each value is checked and inserted once; set operations are O(1) on average.
- Space: O(n). The set may hold all `n` distinct values.
