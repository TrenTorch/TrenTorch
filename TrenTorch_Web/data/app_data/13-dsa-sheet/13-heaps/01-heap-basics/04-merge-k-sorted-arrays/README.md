---
name: sheet-merge-k-sorted-arrays
title: 'Merge K Sorted Arrays'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

`arrays` is a list of `k` lists, each sorted in increasing order. Merge them into **one sorted list**.

For `[[1, 4, 5], [1, 3, 4], [2, 6]]` the answer is `[1, 1, 2, 3, 4, 4, 5, 6]`.

### Examples

**Example 1**

Input:

```python
merge_k_arrays([[1, 4, 5], [1, 3, 4], [2, 6]])
```

Output:

```text
[1, 1, 2, 3, 4, 4, 5, 6]
```

**Example 2**

Input:

```python
merge_k_arrays([[], [1]])
```

Output:

```text
[1]
```

### Constraints

- `0 <= k <= 10000`
- `0 <= total number of values <= 200000`
- `-10**9 <= value <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

The next value of the merged list is the smallest among the **front elements** of all arrays. A min-heap holds exactly those fronts: `(value, array_index, position)`. Pop the smallest, append it to the output, and push the next value from the same array (if any).

The heap never holds more than `k` items, so each of the `N` values costs `O(log k)`: `O(N log k)`. Sorting everything costs `O(N log N)`, and merging pairs of lists one after another costs `O(N * k)` in the worst case.

## Explanation

The tuple carries the array number and the position, so after a pop you know where to read the next value. Equal values compare by array number, so tuples never compare past the integers.
