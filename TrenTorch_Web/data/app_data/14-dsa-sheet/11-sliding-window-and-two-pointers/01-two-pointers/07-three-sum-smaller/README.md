---
name: sheet-three-sum-smaller
title: 'Count Triplets With a Smaller Sum'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: counting-many-answers-at-once
---

## Statement

Return the number of **triples of positions** `i < j < k` with `nums[i] + nums[j] + nums[k] < target`.

For `nums = [-2, 0, 1, 3]` and `target = 2` the answer is `2` (`-2 + 0 + 1` and `-2 + 0 + 3`).

The starter code tries every triple. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
count_triplets_smaller([-2, 0, 1, 3], 2)
```

Output:

```text
2
```

**Example 2**

Input:

```python
count_triplets_smaller([], 0)
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-3000 <= target <= 3000`

## Explanation

After sorting, a successful pair `(lo, hi)` means all positions `lo+1..hi` can play the third role together with `lo`; that is `hi - lo` triples.

### Complexity

- Time: O(n^2). Sort once, then for each first value a two-pointer sweep counts a whole range at once.
- Space: O(n). The sorted copy.
