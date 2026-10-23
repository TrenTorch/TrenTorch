---
name: sheet-count-occurrences
title: 'Count Occurrences'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Beginner
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

## Theory

`nums.count(target)` reads the whole list: `O(n)`. In a sorted list the copies of a value sit in **one block**, so counting them only needs the two ends of that block.

The block runs from the lower bound to the upper bound (the first index `>= target` and the first index `> target`), so the count is `upper - lower`. If the target is absent both bounds are the same index and the answer is `0`, with no special case.

Python gives you both bounds: `bisect.bisect_right(nums, target) - bisect.bisect_left(nums, target)`.

## Explanation

Two binary searches, one with `<` and one with `<=`, return the two bounds; their difference is the block length. It works even when the target is absent, because both searches then stop at the same index.
