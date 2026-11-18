---
name: sheet-four-sum-count
title: 'Four Lists Sum to Zero'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Advanced
theory: four-lists-become-two-pairs
---

## Statement

The four lists `a`, `b`, `c` and `d` have the same length `n`. Return how many tuples of positions `(i, j, k, l)` satisfy `a[i] + b[j] + c[k] + d[l] == 0`. Different positions count separately even when the values are equal.

The starter code tries every tuple. It is correct but far too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2])
```

Output:

```text
2
```

Two tuples work: positions (0, 0, 0, 1) and (1, 1, 0, 0).

**Example 2**

Input:

```python
four_sum_count([0], [0], [0], [0])
```

Output:

```text
1
```

The only tuple adds to 0.

### Constraints

- `0 <= n <= 400`
- `-10**6 <= value <= 10**6`
- All four lists have length `n`.

## Explanation

`Counter(x + y for x in a for y in b)` counts how many ways each sum `a + b` can be made. For each `c + d`, the number of completing pairs is `sums[-(x + y)]`, which is `0` for a missing key. Adding them all counts every tuple once.

### Complexity

- Time: O(n^2). All `n^2` sums of `a` and `b` are counted once, then each of the `n^2` sums of `c` and `d` is one lookup.
- Space: O(n^2). The counter of pair sums.
