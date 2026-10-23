---
name: sheet-first-and-last-position
title: 'First and Last Position'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
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

## Theory

You now have two tools: the **lower bound** (first index with `nums[i] >= target`) and the **upper bound** (first index with `nums[i] > target`). A block of equal values starts at the lower bound and ends just before the upper bound.

So the first position is `lower = lower_bound(target)`, provided `nums[lower] == target` (otherwise the target is absent), and the last position is `upper_bound(target) - 1`. Two binary searches, `O(log n)` in total. A common mistake is to find any match with plain binary search and then walk left and right: with many equal values that walk is `O(n)` again.

## Explanation

`lo` is the lower bound. If it equals `len(nums)` or `nums[lo] != target`, the target is missing. Otherwise the block ends at `upper - 1`, where `upper` is the upper bound found with `<=`. Both searches use the same loop with a different comparison.
