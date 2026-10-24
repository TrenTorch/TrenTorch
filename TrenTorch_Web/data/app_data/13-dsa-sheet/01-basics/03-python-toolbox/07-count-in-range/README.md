---
name: sheet-count-in-range
title: 'Count in Range'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
---

## Statement

`sorted_nums` is sorted in increasing order. Each query is `[lo, hi]` (with `lo <= hi`). For every query, return how many numbers `v` in `sorted_nums` satisfy `lo <= v <= hi`. Return the answers in query order.

### Examples

**Example 1**

Input:

```python
count_in_range([1, 3, 3, 5, 8], [[3, 5], [0, 0], [2, 9]])
```

Output:

```text
[3, 0, 4]
```

The values 3, 3, 5 are inside `[3, 5]`; nothing is `0`; 3, 3, 5, 8 are inside `[2, 9]`.

**Example 2**

Input:

```python
count_in_range([], [[0, 10]])
```

Output:

```text
[0]
```

### Constraints

- `0 <= len(sorted_nums) <= 2 * 10**5`
- `0 <= len(queries) <= 2 * 10**5`
- `0 <= sorted_nums[i], lo, hi <= 10**6`
- Counting each query with a loop over the list is too slow.

## Theory

In a sorted list, all values in a range sit next to each other. So you only need the _positions_ where the range starts and ends, and the count is the difference of the two positions.

`bisect` finds a position in `O(log n)` by binary search. `bisect_left(a, x)` is the index of the first element `>= x`; `bisect_right(a, x)` is the index of the first element `> x`. The numbers in `[lo, hi]` are exactly those between `bisect_left(a, lo)` and `bisect_right(a, hi)`.

Using `bisect_right` for the upper end is what makes `hi` inclusive. Mixing the two functions up is the classic off-by-one.

## Explanation

For each query compute `bisect_right(sorted_nums, hi) - bisect_left(sorted_nums, lo)`. Each query costs `O(log n)`, so `q` queries cost `O(q log n)`.
