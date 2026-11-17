---
name: sheet-first-and-last-position
title: 'First and Last Position'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
theory: first-last-and-how-many
---

## Statement

`nums` is sorted in non-decreasing order and may contain repeated values. Return `[first, last]`: the first and the last index where `target` appears. If it does not appear, return `[-1, -1]`.

### Examples

**Example 1**

Input:

```python
first_and_last([5, 7, 7, 8, 8, 10], 8)
```

Output:

```text
[3, 4]
```

**Example 2**

Input:

```python
first_and_last([5, 7, 7, 8, 8, 10], 6)
```

Output:

```text
[-1, -1]
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in non-decreasing order.
- `-10**9 <= nums[i], target <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Explanation

`lo` is the lower bound. If it equals `len(nums)` or `nums[lo] != target`, the target is missing. Otherwise the block ends at `upper - 1`, where `upper` is the upper bound found with `<=`. Both searches use the same loop with a different comparison.

### Complexity

- Time: O(log n). Two binary searches, each halving its range.
- Space: O(1). A few indices.
