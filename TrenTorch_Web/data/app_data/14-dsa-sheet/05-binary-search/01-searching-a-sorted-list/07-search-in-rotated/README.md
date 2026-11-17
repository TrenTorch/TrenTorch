---
name: sheet-search-in-rotated
title: 'Search in a Rotated List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
theory: searching-a-rotated-list
---

## Statement

A sorted list with **no repeated values** was rotated: some values moved from the front to the back (for example `[0, 1, 2, 4, 5, 6, 7]` became `[4, 5, 6, 7, 0, 1, 2]`). Return the index of `target`, or `-1` if it is not there.

### Examples

**Example 1**

Input:

```python
search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
```

Output:

```text
4
```

**Example 2**

Input:

```python
search_rotated([4, 5, 6, 7, 0, 1, 2], 3)
```

Output:

```text
-1
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- All values are different; the list is a sorted list rotated by some amount.
- `-10**9 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Explanation

After checking `nums[mid] == target`, decide which half is sorted by comparing `nums[lo]` with `nums[mid]`. In the sorted half a simple range test says whether the target is inside; if so, discard the other half, otherwise discard this half. Distinct values make `<=` on the sorted-half test safe.

### Complexity

- Time: O(log n). At every step one half of the range is sorted, which tells which half can hold the target, so the range halves.
- Space: O(1). Three indices.
