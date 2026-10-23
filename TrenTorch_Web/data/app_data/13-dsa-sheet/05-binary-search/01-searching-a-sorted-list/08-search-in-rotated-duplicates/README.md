---
name: sheet-search-in-rotated-duplicates
title: 'Search in a Rotated List With Repeats'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Advanced
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

## Theory

Repeats break one step of the earlier idea. If `nums[lo] == nums[mid] == nums[hi]`, you cannot tell which half is sorted: `[1, 1, 1, 0, 1]` and `[1, 0, 1, 1, 1]` look identical at those three positions.

In that situation the only safe move is to **shrink the range by one on each side** (`lo += 1`, `hi -= 1`): the values you drop are equal to `nums[mid]`, and `nums[mid]` was already checked against the target. Everything else works as before.

That fallback means the worst case is `O(n)` (for example a list of almost all equal values), but typical inputs are `O(log n)`. It is a good example of an algorithm whose worst case is worse than its usual case.

## Explanation

Return `True` when `nums[mid] == target`. If the three boundary values are equal, drop one from both ends. Otherwise decide which half is sorted (`nums[lo] <= nums[mid]` means the left half) and apply the same range test as before to keep the correct half.
