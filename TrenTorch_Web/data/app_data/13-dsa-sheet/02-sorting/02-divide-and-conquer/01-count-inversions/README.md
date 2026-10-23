---
name: sheet-count-inversions
title: 'Count Inversions'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Advanced
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

## Theory

Checking all pairs is `O(n²)`: for `10⁵` values that is about `5 * 10⁹` comparisons.

**Merge sort** can count inversions as a free by-product. Split the list in half, solve each half, then merge. The inversions are of three kinds: both values in the left half, both in the right half, or one in each. The first two are counted by the recursive calls. For the third kind, look at the merge: when a value from the right half is taken _before_ the remaining values of the left half, it is smaller than **all** of them, and each of those left values forms an inversion with it. So add the number of left values still waiting.

Each level of the recursion does `O(n)` work and there are `log₂ n` levels: `O(n log n)`.

## Explanation

`sort(a)` returns the sorted list and its inversion count. Split, recurse, then merge: when taking a value from the right half, add `len(left) - i`, the number of left values not yet used (all of them are larger). Equal values take from the left first, so they are not counted.

The recursion is only `log₂ n` deep (about 17 for `10⁵`), so Python's recursion limit is no problem.
