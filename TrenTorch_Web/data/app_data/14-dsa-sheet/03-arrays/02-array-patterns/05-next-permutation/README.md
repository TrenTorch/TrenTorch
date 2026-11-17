---
name: sheet-next-permutation
title: 'Next Permutation'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Advanced
theory: the-next-arrangement
---

## Statement

Arrangements of the same values can be listed in **dictionary order** (the order you would find them in a dictionary: compare the first value, then the second, and so on). Return the arrangement that comes **right after** `nums`. If `nums` is already the last one (all values from largest to smallest), return the first one: the values sorted in increasing order.

Repeated values are allowed, and the next arrangement must differ from the current one unless all values are equal.

### Examples

**Example 1**

Input:

```python
next_permutation([1, 2, 3])
```

Output:

```text
[1, 3, 2]
```

The next arrangement after 1, 2, 3 is 1, 3, 2.

**Example 2**

Input:

```python
next_permutation([3, 2, 1])
```

Output:

```text
[1, 2, 3]
```

This is the last arrangement, so it wraps to the first: 1, 2, 3.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`

## Explanation

Find `i`, the rightmost index with `a[i] < a[i + 1]`. If there is none, reverse the whole list. Otherwise find the rightmost `j` with `a[j] > a[i]`, swap `a[i]` and `a[j]`, and reverse `a[i + 1:]`. Using `>=` and `<=` carefully (strict comparisons) handles repeated values.

### Complexity

- Time: O(n). Find the pivot, swap, reverse the suffix: each is one scan.
- Space: O(n). A copy of the list, because the input must not change.
