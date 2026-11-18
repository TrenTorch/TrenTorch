---
name: sheet-four-sum
title: 'Four Sum'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
theory: any-number-of-values
---

## Statement

Return all the **different groups of four values** from `nums` that add up to `target`. Each group is written in increasing order, there must be no repeated group, and the list of groups is sorted. Values may be reused only when they appear several times in `nums`.

The starter code tries every group of four positions. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
four_sum([1, 0, -1, 0, -2, 2], 0)
```

Output:

```text
[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
```

The groups are `[-2, -1, 1, 2]`, `[-2, 0, 0, 2]` and `[-1, 0, 0, 1]`.

**Example 2**

Input:

```python
four_sum([2, 2, 2, 2, 2], 8)
```

Output:

```text
[[2, 2, 2, 2]]
```

Only one different group: `[2, 2, 2, 2]`.

### Constraints

- `0 <= len(nums) <= 150`
- `-10**4 <= nums[i] <= 10**4`
- `-4 * 10**4 <= target <= 4 * 10**4`

## Explanation

Two loops fix `i` and `j` (skipping repeats at each level). The inner `lo`/`hi` sweep looks for two values that add up to `target - a[i] - a[j]`. After a match, both pointers move and skip equal values, so each group is recorded once, in sorted order.

### Complexity

- Time: O(n^3). Sort once, fix two values with two loops, then a two-pointer sweep costs O(n).
- Space: O(n). The sorted copy (the result list is extra output).
