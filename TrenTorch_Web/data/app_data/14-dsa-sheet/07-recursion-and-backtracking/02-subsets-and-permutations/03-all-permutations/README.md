---
name: sheet-all-permutations
title: 'All Permutations'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
theory: all-orderings
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

## Explanation

`used[j]` says whether `a[j]` is already in the current permutation. When `current` has `len(a)` values, record a copy. Otherwise try every unused value in sorted order: mark, append, recurse, then undo both.

### Complexity

- Time: O(n * n!). There are `n!` permutations, and each leaf costs `O(n)` to scan and copy.
- Space: O(n * n!). The output; the recursion adds only `O(n)`.
