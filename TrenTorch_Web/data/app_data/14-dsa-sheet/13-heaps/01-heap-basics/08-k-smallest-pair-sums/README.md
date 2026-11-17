---
name: sheet-k-smallest-pair-sums
title: 'K Smallest Pair Sums'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Advanced
theory: pairs-are-secretly-sorted-lists
---

## Statement

`nums1` and `nums2` are sorted in increasing order. Consider every pair `(a, b)` with `a` from `nums1` and `b` from `nums2`. Return the **`k` smallest sums** `a + b`, in increasing order (if there are fewer than `k` pairs, return all sums).

For `nums1 = [1, 7, 11]`, `nums2 = [2, 4, 6]` and `k = 3` the answer is `[3, 5, 7]`.

The starter code builds the sums of all pairs and sorts them. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
k_smallest_pair_sums([1, 7, 11], [2, 4, 6], 3)
```

Output:

```text
[3, 5, 7]
```

**Example 2**

Input:

```python
k_smallest_pair_sums([1, 1, 2], [1, 2, 3], 2)
```

Output:

```text
[2, 2]
```

### Constraints

- `0 <= len(nums1), len(nums2) <= 100000`
- `0 <= k <= 10000`
- `-10**9 <= value <= 10**9`

## Explanation

Starting with the first `k` rows is enough: a row index of `k` or more can never be among the `k` smallest sums, since there are `k` rows before it that are all at most as large.

### Complexity

- Time: O(k log k). A heap with at most `k` entries, one pop and one push per answer.
- Space: O(k). The heap (the result is output).
