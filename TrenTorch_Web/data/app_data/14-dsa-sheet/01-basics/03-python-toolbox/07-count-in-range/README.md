---
name: sheet-count-in-range
title: 'Count in Range'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
theory: binary-search-with-bisect
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

## Explanation

For each query compute `bisect_right(sorted_nums, hi) - bisect_left(sorted_nums, lo)`. Each query costs `O(log n)`, so `q` queries cost `O(q log n)`.

### Complexity

- Time: O(q log n). Two binary searches per query on a sorted list of `n` values.
- Space: O(1). Nothing besides the answer list.
