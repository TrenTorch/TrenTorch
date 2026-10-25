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

**Explanation:** The 10th ugly number is 12 because the sequence of ugly numbers up to the 10th is 1, 2, 3, 4, 5, 6, 8, 9, 10, 12.

**Example 2**

Input:

```python
nth_ugly_number(1)
```

Output:

```text
1
```

**Explanation:** The 1st ugly number is 1 because the sequence starts with 1.

### Constraints

- `1 <= n <= 100000`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Every ugly number except 1 is a smaller ugly number times 2, 3 or 5. So generate them in increasing order with a **min-heap**: start with `1`. Pop the smallest `x`, it is the next ugly number; push `2x`, `3x` and `5x` (if not seen yet; a set avoids duplicates such as `6 = 2 * 3 = 3 * 2`). The `n`-th pop is the answer.

The heap needs `O(n log n)`. There is also a neat `O(n)` method with three pointers into the list of ugly numbers found so far: the next ugly number is the smallest of `2 * u[i2]`, `3 * u[i3]` and `5 * u[i5]`, and the pointers that produced the minimum advance.

## Explanation

`seen` keeps duplicates out of the heap. The loop pops `n - 1` numbers and the next pop is the answer; here the three-pointer version is shown because it is `O(n)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                       | Variables                                                       |
| ----------------------------------------------------- | --------------------------------------------------------------- |
| `ugly = [1]`                                          | `ugly = [1]`                                                    |
| `nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)` | `ugly = [1, 2], i2 = 1, i3 = 0, i5 = 0, nxt = 3`                |
| `ugly.append(nxt)`                                    | `ugly = [1, 2, 3, 4], i3 = 1, nxt = 4`                          |
| `nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)` | `ugly = [1, 2, 3, 4, 5], i2 = 2, i5 = 1, nxt = 6`               |
| `nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)` | `ugly = [1, 2, 3, 4, 5, 6], i2 = 3, i3 = 2, nxt = 8`            |
| `i3 += 1`                                             | `ugly = [1, 2, 3, 4, 5, 6, 8, 9], i2 = 4, i3 = 3, nxt = 9`      |
| `i5 += 1`                                             | `ugly = [1, 2, 3, 4, 5, 6, 8, 9, 10], i2 = 5, i5 = 2, nxt = 10` |
| `return`                                              | `returned = 12`                                                 |

### Complexity

- Time: O(n).
- Extra space: O(n).
- The brute force takes O(n log n).
