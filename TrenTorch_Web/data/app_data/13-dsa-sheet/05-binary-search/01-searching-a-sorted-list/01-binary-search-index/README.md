---
name: sheet-binary-search-index
title: 'Binary Search'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Beginner
---

## Statement

`nums` is sorted in increasing order and has **no repeated values**. Return the index of `target`, or `-1` if it is not in the list.

The starter code reads the list one value at a time. The big tests only allow a handful of reads, so make each search halve the range.

### Examples

**Example 1**

Input:

```python
binary_search_index([-1, 0, 3, 5, 9, 12], 9)
```

Output:

```text
4
```

**Example 2**

Input:

```python
binary_search_index([-1, 0, 3, 5, 9, 12], 2)
```

Output:

```text
-1
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in increasing order with different values.
- `-10**9 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

A scan checks the values one by one: `O(n)` reads. In a **sorted** list one comparison can rule out half of what is left. Look at the middle value: if it is the target, you are done; if the target is smaller, it can only be in the left half; if bigger, only in the right half. Repeat on the half that remains.

Each step halves the range, so `n` values need about `log₂ n` steps: 18 for 200,000 values, 30 for a billion. This is **binary search**.

Keep two boundaries `lo` and `hi` that always bracket where the target can still be, and loop while `lo <= hi`. Set `mid = (lo + hi) // 2` and move a boundary to `mid + 1` or `mid - 1`, never to `mid` itself: that guarantees the range shrinks, so the loop ends.

## Explanation

`nums[mid] == target` returns `mid`. A smaller value means everything up to `mid` is too small, so `lo = mid + 1`. A bigger value means `hi = mid - 1`. When `lo > hi` the range is empty and the target is not present. A search reads about `log₂ n` values.
