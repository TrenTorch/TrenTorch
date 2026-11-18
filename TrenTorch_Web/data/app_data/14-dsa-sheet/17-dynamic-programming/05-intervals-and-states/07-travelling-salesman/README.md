---
name: sheet-travelling-salesman
title: 'Travelling Salesman (Small)'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: the-travelling-salesman
---

## Statement

`dist[i][j]` is the distance from city `i` to city `j` (it may differ from `dist[j][i]`). Starting at city `0`, visit **every city exactly once** and come back to city `0`. Return the **shortest total distance**. With one city the answer is `0`.

For `[[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]` the answer is `80`.

The starter code tries every order of the cities. It is correct but too slow for more than 9 or 10 cities.

### Examples

**Example 1**

Input:

```python
tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])
```

Output:

```text
80
```

**Example 2**

Input:

```python
tsp([[0, 5], [7, 0]])
```

Output:

```text
12
```

### Constraints

- `0 <= number of cities <= 13`
- `1 <= dist[i][j] <= 100` for `i != j`

## Explanation

Masks are processed in increasing order, so a smaller mask is always finished before it is extended. Bit 0 (city 0) is set from the start.

### Complexity

- Time: O(n^2 * 2^n). Held-Karp: `2^n` subsets, each with `n` last cities and `n` next cities.
- Space: O(n * 2^n). The table of costs per subset and last city.
