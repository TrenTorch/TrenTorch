---
name: sheet-search-in-rotated-duplicates
title: 'Search in a Rotated List With Repeats'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Advanced
theory: rotated-lists-with-repeats
---

## Statement

Like the previous question, but the values **may repeat**. A sorted list was rotated. Return `True` if `target` is in the list, `False` otherwise.

### Examples

**Example 1**

Input:

```python
search_rotated_duplicates([2, 5, 6, 0, 0, 1, 2], 0)
```

Output:

```text
True
```

**Example 2**

Input:

```python
search_rotated_duplicates([2, 5, 6, 0, 0, 1, 2], 3)
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- The list is a non-decreasing list rotated by some amount.
- `-10**9 <= nums[i], target <= 10**9`

## Explanation

Return `True` when `nums[mid] == target`. If the three boundary values are equal, drop one from both ends. Otherwise decide which half is sorted (`nums[lo] <= nums[mid]` means the left half) and apply the same range test as before to keep the correct half.

### Complexity

- Time: O(n) worst case, O(log n) when few values repeat. When `nums[lo] == nums[mid] == nums[hi]` nothing tells which half is sorted, so only one end can be dropped; a list of equal values forces a linear scan, and no algorithm can do better in that case.
- Space: O(1). Three indices.
