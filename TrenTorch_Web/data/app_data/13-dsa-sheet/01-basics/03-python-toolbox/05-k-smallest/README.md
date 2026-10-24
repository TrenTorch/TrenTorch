---
name: sheet-k-smallest
title: 'K Smallest Numbers'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
---

## Statement

Return the `k` smallest numbers of `nums` in increasing order. If `k` is larger than the list, return all of them sorted. Equal values count separately.

### Examples

**Example 1**

Input:

```python
k_smallest([7, 2, 9, 4, 2], 3)
```

Output:

```text
[2, 2, 4]
```

**Example 2**

Input:

```python
k_smallest([5, 1], 10)
```

Output:

```text
[1, 5]
```

### Constraints

- `0 <= len(nums) <= 10**6`
- `0 <= k <= 10**6`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Sorting everything costs `O(n log n)` even if you only need a few results. A **heap** is a structure that always gives you its smallest (or largest) item quickly. `heapq.nsmallest(k, nums)` keeps only the `k` best candidates while it scans the list, which is `O(n log k)`. When `k` is small compared to `n` that is a big saving.

Python's `heapq` is a _min_-heap stored in a plain list. The functions `heappush`, `heappop`, `nsmallest` and `nlargest` cover most interview problems. For a tiny `k` it also beats `sorted(nums)[:k]` on memory, since it never builds a second full-size list.

## Explanation

`heapq.nsmallest(k, nums)` returns the `k` smallest values already sorted ascending, and returns everything sorted when `k >= len(nums)`.

`sorted(nums)[:k]` gives the same answer and is fine at this size; the heap version scales better when `k` is much smaller than `n`.
