---
name: sheet-minimum-arrows-to-burst-balloons
title: 'Minimum Arrows to Burst Balloons'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
---

## Statement

Balloons are drawn on a wall as horizontal segments `[x_start, x_end]`. An arrow shot **straight up** at position `x` bursts every balloon with `x_start <= x <= x_end`. Return the **fewest arrows** that burst all balloons.

For `[[10, 16], [2, 8], [1, 6], [7, 12]]` the answer is `2`.

### Examples

**Example 1**

Input:

```python
min_arrows([[10, 16], [2, 8], [1, 6], [7, 12]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_arrows([[1, 2], [3, 4], [5, 6], [7, 8]])
```

Output:

```text
4
```

### Constraints

- `0 <= len(points) <= 200000`
- `-10**9 <= x_start < x_end <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

This is the interval-overlap problem again, seen differently: one arrow can burst a group of balloons that all share a common point. Sort by **end**, and shoot the first arrow at the **end** of the first balloon: that position bursts as many of the following overlapping balloons as possible (any balloon starting at or before it, still ahead in the order).

Skip all balloons that start at or before the arrow position; the next balloon that starts **after** it needs a new arrow, placed at its end. Count the arrows. `O(n log n)`.

## Explanation

`arrow` is the position of the last arrow. A balloon with `x_start <= arrow` is already burst (its end is at least the arrow, thanks to the sorting).
