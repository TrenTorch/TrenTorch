---
name: sheet-k-closest-points
title: 'K Closest Points to the Origin'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

Return the `k` points of `points` that are **closest to the origin** `(0, 0)`, using the straight-line distance. Sort them by squared distance `x² + y²`, nearest first; points at the same distance go by `x` and then by `y` (increasing). Points can repeat.

For `points = [[1, 3], [-2, 2]]` and `k = 1` the answer is `[[-2, 2]]`.

### Examples

**Example 1**

Input:

```python
k_closest([[1, 3], [-2, 2]], 1)
```

Output:

```text
[[-2, 2]]
```

**Example 2**

Input:

```python
k_closest([[3, 3], [5, -1], [-2, 4]], 2)
```

Output:

```text
[[3, 3], [-2, 4]]
```

### Constraints

- `0 <= k <= len(points) <= 100000`
- `-10**4 <= x, y <= 10**4`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Sorting all `n` points costs `O(n log n)`. When `k` is much smaller than `n` you can do better by keeping only the `k` best so far in a **max-heap of size `k`** (the farthest of the current `k` on top). For each new point: push it; if the heap now has more than `k` points, pop the farthest. At the end the heap holds the `k` closest points. This costs `O(n log k)`.

Python's `heapq.nsmallest(k, points, key=...)` does exactly this for you. Compare squared distances: no square root is needed to compare which is closer.

## Explanation

The key `(x*x + y*y, x, y)` gives the required order, including the tie-breaks. `nsmallest` returns the `k` smallest items in sorted order.
