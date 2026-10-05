---
name: numpy-unique-counting
title: 'Unique Values & Counting'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that answer "which distinct values are there, and how often?". `distinct` returns the sorted distinct values, `value_counts` returns those values with their counts, `first_positions` returns where each distinct value first occurs, `codes` turns every element into the integer index of its value among the distinct ones, `mode` returns the most frequent value (the smallest when several tie), and `unique_in_order` returns the distinct values in the order they first appear.

## Theory

### `np.unique` does several jobs

```python
a = np.array([3, 1, 2, 3, 1, 3])
values, index, inverse, counts = np.unique(a, return_index=True,
                                           return_inverse=True, return_counts=True)
# values  [1, 2, 3]            the sorted distinct values
# index   [1, 2, 0]            first position of each value in a
# inverse [2, 0, 1, 2, 0, 2]   for every element, its index in `values`
# counts  [2, 1, 3]            how often each value occurs
```

`values[inverse]` reconstructs `a`, which is why `inverse` is the standard way to turn labels into integer codes (for example before building one-hot vectors).

### Counting

`counts` makes a histogram of a discrete variable. The most frequent value is `values[np.argmax(counts)]`; because `values` is sorted and `argmax` returns the **first** maximum, ties automatically resolve to the smallest value.

### First-appearance order

`np.unique` always sorts. To list distinct values in the order they first appear, use the first positions and sort _those_:

```python
values, index = np.unique(a, return_index=True)
a[np.sort(index)]          # [3, 1, 2]
```

### Cost

`unique` sorts its input, so it is $O(n \log n)$. For small integer values, `np.bincount(a)` counts in $O(n)$ but needs non-negative integers.

### How NumPy implements this

`np.unique` flattens the array, sorts it (an `argsort` when indices are requested), then marks the positions where a value differs from its predecessor with a boolean mask; the counts are the gaps between those marks.

## Explanation

Everything comes from one `np.unique` call. `distinct` and `value_counts` use its values and counts. `first_positions` uses `return_index`. `codes` uses `return_inverse`. `mode` takes the value at the first maximum count, which is the smallest value among ties because the values are sorted. `unique_in_order` takes the first positions, sorts them, and reads the array at those positions.
