---
name: sheet-all-permutations
title: 'All Permutations'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
---

## Statement

`nums` holds **different** values. Return every **ordering** (permutation) of them, listed in **dictionary order** of the orderings. For `[1, 2, 3]`: `[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]`.

### Examples

**Example 1**

Input:

```python
all_permutations([1, 2, 3])
```

Output:

```text
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

**Example 2**

Input:

```python
all_permutations([7])
```

Output:

```text
[[7]]
```

### Constraints

- `0 <= len(nums) <= 7`
- All values are different.
- `-100 <= nums[i] <= 100`

## Theory

A permutation is built by choosing **which value goes in each position**, one position at a time: any value that has **not been used yet** can go next. Keep a `used` flag per value. The recursive function fills position `len(current)`; it loops over all values, skips used ones, places one, recurses, and un-places it.

With the values sorted, trying them in increasing order produces the permutations in dictionary order.

There are `n!` permutations (5,040 for `n = 7`), which grows faster than `2^n`. That is the true cost of the problem, not a flaw in the method.

## Explanation

`used[j]` says whether `a[j]` is already in the current permutation. When `current` has `len(a)` values, record a copy. Otherwise try every unused value in sorted order: mark, append, recurse, then undo both.
