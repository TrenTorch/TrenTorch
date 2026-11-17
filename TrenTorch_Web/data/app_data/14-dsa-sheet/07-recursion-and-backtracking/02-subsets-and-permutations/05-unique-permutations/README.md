---
name: sheet-unique-permutations
title: 'Permutations With Repeated Values'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
theory: repeated-values-in-permutations
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

## Explanation

The condition says: if `a[j]` has a twin `a[j - 1]` that is still unused, then using `a[j]` first would just be the twin swapped in, a repeat. So equal values are placed left to right in the sorted order.

### Complexity

- Time: O(n * n!). At most `n!` permutations, each costing `O(n)` to scan and copy; the skip rule never builds a duplicate.
- Space: O(n * n!). The output; the recursion adds only `O(n)`.
