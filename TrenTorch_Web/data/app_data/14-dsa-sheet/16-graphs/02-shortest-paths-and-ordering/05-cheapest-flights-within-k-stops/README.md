---
name: sheet-cheapest-flights-within-k-stops
title: 'Cheapest Flights Within K Stops'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: cheapest-flights-within-k-stops
---

## Statement

There are `n` cities and flights `[from, to, price]` (one-way). Return the **cheapest price** to travel from `src` to `dst` with **at most `k` stops** in between (so at most `k + 1` flights), or `-1` if impossible.

For `n = 4`, `flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]`, `src = 0`, `dst = 3` and `k = 1` the answer is `700`.

### Examples

**Example 1**

Input:

```python
cheapest_price(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1)
```

Output:

```text
700
```

**Example 2**

Input:

```python
cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0)
```

Output:

```text
500
```

### Constraints

- `1 <= n <= 1000`
- `0 <= len(flights) <= 5000`
- `0 <= price <= 10**4`
- `0 <= k <= n`

## Explanation

`nxt` starts as a copy of `best`. Each flight is relaxed from the old `best`, so a path gains at most one flight per round.

### Complexity

- Time: O(k * e). Bellman-Ford limited to `k + 1` rounds, each round relaxes every flight once.
- Space: O(n). Two arrays of distances.
