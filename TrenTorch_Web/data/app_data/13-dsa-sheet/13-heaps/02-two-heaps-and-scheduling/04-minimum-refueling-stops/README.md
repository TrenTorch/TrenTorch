---
name: sheet-minimum-refueling-stops
title: 'Minimum Refueling Stops'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
---

## Statement

A car starts at position 0 with `start_fuel` units of fuel; one unit of fuel moves it one mile. There are gas stations `stations[i] = [position, fuel]` sorted by position; stopping at a station lets you take **all** its fuel (your tank has no limit). Return the **fewest stops** needed to reach `target`, or `-1` if impossible. If you can reach the target without stopping the answer is `0`.

For `target = 100`, `start_fuel = 10` and `stations = [[10, 60], [20, 30], [30, 30], [60, 40]]` the answer is `2`.

The starter code tracks the best reach for every number of stops. It is correct but too slow for many stations.

### Examples

**Example 1**

Input:

```python
min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]])
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_refuel_stops(100, 1, [[10, 100]])
```

Output:

```text
-1
```

### Constraints

- `1 <= target <= 10**9`
- `0 <= start_fuel <= 10**9`
- `0 <= len(stations) <= 100000`, sorted by position, positions below `target`
- `1 <= fuel <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

You do not need to decide where to stop at the time you drive past a station. Think backwards: drive as far as the fuel allows, and **only when you run out**, imagine you had stopped at the **best station you already passed** (the one with the most fuel). Passing stations are collected in a **max-heap of their fuel amounts**.

Loop: while the current reach is below the target, add all stations within reach to the heap; if the heap is empty you are stuck (`-1`); otherwise take the largest fuel (one more stop) and add it to your reach. Count the stops.

This "decide later with a heap" trick turns a search into a greedy algorithm: `O(n log n)`.

## Explanation

`reach` is the farthest position possible with the current fuel. Stations are pushed into the heap as they come within reach, and a refuel is only taken when needed.
