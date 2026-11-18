---
name: sheet-count-occurrences
title: 'Count Occurrences'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Beginner
theory: first-last-and-how-many
---

## Statement

`nums` is sorted in non-decreasing order and may contain repeated values. Return how many times `target` appears.

### Examples

**Example 1**

Input:

```python
count_occurrences([1, 2, 2, 2, 3], 2)
```

Output:

```text
3
```

**Example 2**

Input:

```python
count_occurrences([1, 3], 2)
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in non-decreasing order.
- `-10**9 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Explanation

Two binary searches, one with `<` and one with `<=`, return the two bounds; their difference is the block length. It works even when the target is absent, because both searches then stop at the same index.

### Complexity

- Time: O(log n). Two binary searches (`bisect_left` and `bisect_right`).
- Space: O(1). Nothing is stored.
