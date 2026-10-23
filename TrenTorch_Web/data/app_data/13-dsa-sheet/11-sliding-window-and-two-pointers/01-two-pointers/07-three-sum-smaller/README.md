---
name: sheet-three-sum-smaller
title: 'Count Triplets With a Smaller Sum'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
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

## Theory

The order of positions does not change the sum, so sort the list: counting triples of **values** (as sets of three positions) is the same. Fix `i`, then use two pointers `lo = i + 1` and `hi = n - 1`.

If `a[i] + a[lo] + a[hi] < target`, then **every** `k` between `lo + 1` and `hi` also works with `lo` (they are smaller than `a[hi]`): add `hi - lo` triples at once, and move `lo` forward. Otherwise the sum is too big: move `hi` back.

Counting many answers in one step ("everything between the pointers also works") is the common trick in two-pointer counting questions. `O(n²)`.

## Explanation

After sorting, a successful pair `(lo, hi)` means all positions `lo+1..hi` can play the third role together with `lo`; that is `hi - lo` triples.
