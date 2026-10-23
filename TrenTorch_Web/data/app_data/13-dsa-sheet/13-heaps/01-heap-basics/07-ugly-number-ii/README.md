---
name: sheet-ugly-number-ii
title: 'The Nth Ugly Number'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

An **ugly number** is a positive whole number whose only prime factors are `2`, `3` and `5`. The first ones are `1, 2, 3, 4, 5, 6, 8, 9, 10, 12, ...`. Return the **`n`-th** ugly number (`n = 1` gives `1`).

For `n = 10` the answer is `12`.

The starter code tests every whole number in turn. It is correct but too slow when `n` is large.

### Examples

**Example 1**

Input:

```python
nth_ugly_number(10)
```

Output:

```text
12
```

**Example 2**

Input:

```python
nth_ugly_number(1)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 100000`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Every ugly number except 1 is a smaller ugly number times 2, 3 or 5. So generate them in increasing order with a **min-heap**: start with `1`. Pop the smallest `x`, it is the next ugly number; push `2x`, `3x` and `5x` (if not seen yet; a set avoids duplicates such as `6 = 2 * 3 = 3 * 2`). The `n`-th pop is the answer.

The heap needs `O(n log n)`. There is also a neat `O(n)` method with three pointers into the list of ugly numbers found so far: the next ugly number is the smallest of `2 * u[i2]`, `3 * u[i3]` and `5 * u[i5]`, and the pointers that produced the minimum advance.

## Explanation

`seen` keeps duplicates out of the heap. The loop pops `n - 1` numbers and the next pop is the answer; here the three-pointer version is shown because it is `O(n)`.
