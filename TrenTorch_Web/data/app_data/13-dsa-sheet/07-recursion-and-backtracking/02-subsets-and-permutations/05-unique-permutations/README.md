---
name: sheet-unique-permutations
title: 'Permutations With Repeated Values'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
---

## Statement

`nums` may contain **repeated values**. Return every **different ordering**, listed in dictionary order. For `[1, 1, 2]`: `[1,1,2], [1,2,1], [2,1,1]`.

### Examples

**Example 1**

Input:

```python
unique_permutations([1, 1, 2])
```

Output:

```text
[[1, 1, 2], [1, 2, 1], [2, 1, 1]]
```

**Example 2**

Input:

```python
unique_permutations([3, 3])
```

Output:

```text
[[3, 3]]
```

### Constraints

- `0 <= len(nums) <= 8`
- `-100 <= nums[i] <= 100`

## Theory

The permutations recursion produces repeats when equal values are swapped around. With `[1, 1, 2]` the two `1`s are interchangeable, so choosing "first `1` then second `1`" or "second `1` then first `1`" gives the same ordering.

Sort the values, and add one rule: **skip a value if it equals the previous value and that previous value is not currently in use**. In code: `if j > 0 and a[j] == a[j - 1] and not used[j - 1]: continue`. It forces equal values to be used **in their sorted order**, so each distinct ordering is built exactly once.

This is the permutation version of "skip duplicates at the same level".

## Explanation

The condition says: if `a[j]` has a twin `a[j - 1]` that is still unused, then using `a[j]` first would just be the twin swapped in, a repeat. So equal values are placed left to right in the sorted order.
