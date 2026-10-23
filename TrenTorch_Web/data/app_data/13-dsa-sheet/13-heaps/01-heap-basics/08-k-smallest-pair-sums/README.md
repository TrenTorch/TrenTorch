---
name: sheet-k-smallest-pair-sums
title: 'K Smallest Pair Sums'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Advanced
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

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

There are `n * m` pairs, but you only need the first `k`. Think of the pairs as a grid: `sum(i, j) = nums1[i] + nums2[j]` increases along each row and each column. The smallest is `(0, 0)`. After taking `(i, j)`, the next candidates are `(i + 1, j)` and `(i, j + 1)`.

A min-heap holds the candidates `(sum, i, j)`. Start with `(0, 0)` ... or, simpler, with `(i, 0)` for the first `k` values of `nums1`, and when you pop `(i, j)`, push `(i, j + 1)` only. After `k` pops you have the answer. The heap never holds more than `min(n, k)` items: `O(k log k)`.

## Explanation

Starting with the first `k` rows is enough: a row index of `k` or more can never be among the `k` smallest sums, since there are `k` rows before it that are all at most as large.
