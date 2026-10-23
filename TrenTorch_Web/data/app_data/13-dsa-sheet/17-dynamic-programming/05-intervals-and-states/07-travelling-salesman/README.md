---
name: sheet-travelling-salesman
title: 'Travelling Salesman (Small)'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Trying all `(n - 1)!` orders is hopeless for 13 cities (479 million). But the future of a trip depends only on **which cities are already visited** and **where you are now**, not on the order you used. That is a state: `(visited set, current city)`, with `2^n × n` states, which is feasible for `n` up to about 20.

Store the visited set as a **bitmask**. **State:** `best[mask][last]`, the shortest path starting at city 0, visiting exactly the cities of `mask`, and ending at `last`. **Transition:** extend by an unvisited city `nxt`: `best[mask | 1 << nxt][nxt] = min(best[mask][last] + dist[last][nxt])`. **Answer:** `min(best[all][last] + dist[last][0])`. `O(2^n × n²)`.

## Explanation

Masks are processed in increasing order, so a smaller mask is always finished before it is extended. Bit 0 (city 0) is set from the start.
