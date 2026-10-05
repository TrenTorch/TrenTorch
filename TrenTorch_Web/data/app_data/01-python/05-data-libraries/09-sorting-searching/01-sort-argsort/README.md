---
name: numpy-sort-argsort
title: 'Sorting & argsort'
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that sort an array and, more usefully, find _where_ each element would go. `sorted_copy` returns a sorted copy and leaves the input alone, `sort_order` returns the indices that would sort the array (a stable `argsort`), `rank_of` turns that order into each element's position, `descending_order` is the stable order from largest to smallest, and `sort_rows_by_column` reorders the rows of a 2D array by one column. Ties always keep their original relative order (a _stable_ sort).

## Theory

### Sorting values and sorting positions

`np.sort(a)` returns a sorted **copy**; `a.sort()` sorts **in place** and returns `None`. `np.argsort(a)` returns the **indices** that would sort `a`:

```python
a = np.array([30, 10, 20])
np.sort(a)      # [10, 20, 30]
np.argsort(a)   # [1, 2, 0]   a[1]=10, a[2]=20, a[0]=30
a[np.argsort(a)]  # [10, 20, 30]
```

Indices are more useful than values because one ordering can reorder several arrays at once (names by scores, rows by a key).

### Stable sorting

When two elements are equal, a **stable** sort keeps them in their original order. `np.argsort(a, kind="stable")` guarantees it; the default `quicksort` does not. Stability matters whenever ties exist and the result must be reproducible, and it is what makes "sort by B, then by A" work as two passes.

### Rank is the inverse of the order

`order = np.argsort(a, kind="stable")` says "the element at position `order[0]` is the smallest". The **rank** of each element is the opposite question: "what position does element `i` take?". It is the inverse permutation:

```python
rank = np.empty_like(order)
rank[order] = np.arange(len(a))
```

### Descending order

For numbers, sorting `-a` ascending gives `a` descending: `np.argsort(-a, kind="stable")` keeps tied elements in their original order, which `np.argsort(a)[::-1]` would not (it reverses them).

### Sorting rows by a column

`m[np.argsort(m[:, c], kind="stable")]` reorders whole rows by the values in column `c`.

### How NumPy implements this

`sort` and `argsort` use introsort (quicksort with a heapsort fallback) by default, and a radix/merge sort for `kind="stable"`. `argsort` returns an integer index array of the same length, so it costs $O(n \log n)$ time and $O(n)$ extra memory.

## Explanation

`sorted_copy` is `np.sort`, which copies. `sort_order` is a stable `argsort`. `rank_of` writes the positions `0..n-1` through the order, so `rank[order[i]] = i`. `descending_order` sorts the negated values stably, so ties keep their original order. `sort_rows_by_column` indexes the rows with the stable order of the chosen column.
