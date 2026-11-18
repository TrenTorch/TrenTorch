---
name: sheet-count-inversions
title: 'Count Inversions'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Advanced
theory: counting-while-merging
---

## Statement

An **inversion** is a pair of positions `i < j` where `nums[i] > nums[j]`: two values that are the wrong way round. Count them.

The starter code checks every pair. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
count_inversions([3, 1, 2])
```

Output:

```text
2
```

The inversions are (3, 1) and (3, 2).

**Example 2**

Input:

```python
count_inversions([1, 2, 3])
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 5 * 10**4`
- `-10**9 <= nums[i] <= 10**9`
- Equal values are not an inversion.
- The answer can be about `1.25 * 10**9`.

## Explanation

`sort(a)` returns the sorted list and its inversion count. Split, recurse, then merge: when taking a value from the right half, add `len(left) - i`, the number of left values not yet used (all of them are larger). Equal values take from the left first, so they are not counted.

The recursion is only `log₂ n` deep (about 17 for `10⁵`), so Python's recursion limit is no problem.

### Complexity

- Time: O(n log n). Merge sort has `log n` levels and every level merges `n` values; the cross inversions are counted during each merge.
- Space: O(n). The merged lists on the recursion path add up to `n`.
