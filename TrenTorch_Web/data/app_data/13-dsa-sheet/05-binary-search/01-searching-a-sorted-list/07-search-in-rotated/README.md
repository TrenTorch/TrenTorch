---
name: sheet-search-in-rotated
title: 'Search in a Rotated List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
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

## Theory

A rotated sorted list is two sorted pieces glued together, so plain binary search no longer applies. But at **every** step, at least one half of the current range is still perfectly sorted. That is enough.

Look at `nums[lo]` and `nums[mid]`. If `nums[lo] <= nums[mid]`, the **left half** is sorted. Check whether the target lies inside that sorted half (`nums[lo] <= target < nums[mid]`): if yes keep the left half, otherwise the target can only be on the right. If the left half is not sorted, the **right half** must be: check `nums[mid] < target <= nums[hi]` the same way.

Each step halves the range and reads a constant number of values: `O(log n)`.

## Explanation

After checking `nums[mid] == target`, decide which half is sorted by comparing `nums[lo]` with `nums[mid]`. In the sorted half a simple range test says whether the target is inside; if so, discard the other half, otherwise discard this half. Distinct values make `<=` on the sorted-half test safe.
