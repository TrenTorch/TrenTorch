---
name: sheet-four-sum
title: 'Four Sum'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
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

## Theory

This is **Three Sum** with one more loop. Sort the list, fix the two smallest values `a[i]` and `a[j]` with two nested loops, and find the remaining two with the same two-pointer sweep from both ends. That gives `O(n³)`, a big step down from the `O(n⁴)` of four loops.

The same idea generalises: `k`-Sum costs `O(n^(k-1))` with this method. For `k = 2` it is the sorted two-pointer pair search.

Duplicates are handled exactly like in Three Sum: skip a repeated `a[i]` and a repeated `a[j]` (relative to the previous choice at that level), and skip equal values at both pointers after a match.

## Explanation

Two loops fix `i` and `j` (skipping repeats at each level). The inner `lo`/`hi` sweep looks for two values that add up to `target - a[i] - a[j]`. After a match, both pointers move and skip equal values, so each group is recorded once, in sorted order.
