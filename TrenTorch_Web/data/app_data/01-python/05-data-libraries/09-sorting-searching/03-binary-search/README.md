---
name: numpy-binary-search-bins
title: 'Binary Search, Bins & digitize'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions that search a **sorted** array without scanning it. `insertion_points` returns where values would be inserted to keep the order, `count_between` counts how many elements lie in a closed range using two such searches, `bucketize` assigns every value to the interval between consecutive edges, `nearest_value` returns the element closest to a target, and `is_present` tests membership. All of them must be vectorised (no Python loop over the values).

## Theory

### Binary search finds a position in $O(\log n)$

`np.searchsorted(sorted_a, v)` finds, for each value `v`, the index where it would be inserted to keep `sorted_a` sorted, by repeatedly halving the search interval. It needs a sorted array and works on many values at once:

```python
a = np.array([10, 20, 20, 30])
np.searchsorted(a, 20, side="left")    # 1   before the existing 20s
np.searchsorted(a, 20, side="right")   # 3   after the existing 20s
np.searchsorted(a, [5, 25, 99])        # [0, 3, 4]
```

`side="left"` returns the first valid position, `side="right"` the last. The difference between them is how many copies of the value exist.

### Counting in a range

The number of elements with $lo \le x \le hi$ in a sorted array is

$$
\text{searchsorted}(a, hi, \text{right}) - \text{searchsorted}(a, lo, \text{left})
$$

two $O(\log n)$ searches instead of an $O(n)$ scan.

### Bucketing with digitize

`np.digitize(v, edges)` (equivalently `np.searchsorted(edges, v, side="right")`) returns the **bin index**: how many edges are `<=` the value. With edges `[10, 20, 30]`: values below 10 get 0, `[10, 20)` gets 1, `[20, 30)` gets 2, and 30 or more gets 3.

### Nearest neighbour

The nearest element to `x` is one of the two neighbours around its insertion point `i`: `a[i-1]` or `a[i]`. Clamp `i` at the ends and compare the two distances.

### Membership

`v` is in `a` exactly when the element at its insertion point equals it (and the point is inside the array).

### How NumPy implements this

`searchsorted` is a loop of binary searches written in C, one per query value; it does not require the queries to be sorted, but it is faster when they are because the memory accesses stay close together.

## Explanation

`insertion_points` is `np.searchsorted` with the requested side. `count_between` subtracts the left insertion point of `lo` from the right insertion point of `hi`. `bucketize` is `searchsorted(edges, values, side="right")`, which counts how many edges are less than or equal to each value. `nearest_value` finds the insertion point, clamps it, and for each query picks the lower neighbour when it is at least as close (so ties go to the smaller value). `is_present` clamps the insertion point and compares the element found there with the query.
