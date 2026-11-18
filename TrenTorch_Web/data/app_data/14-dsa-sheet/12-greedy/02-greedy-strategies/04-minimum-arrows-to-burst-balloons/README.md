---
name: sheet-minimum-arrows-to-burst-balloons
title: 'Minimum Arrows to Burst Balloons'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
theory: fewest-arrows-for-balloons
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

## Explanation

`arrow` is the position of the last arrow. A balloon with `x_start <= arrow` is already burst (its end is at least the arrow, thanks to the sorting).

### Complexity

- Time: O(n log n). Sorting by end dominates; the scan is one pass.
- Space: O(n). The sorted list.
