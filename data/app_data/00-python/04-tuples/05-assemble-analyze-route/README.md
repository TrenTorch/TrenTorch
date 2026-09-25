---
name: python-tuples-assemble-analyze-route
title: 'Assemble: Analyze a Route of Grid Points'
tags: [python-tuples, python-dicts]
difficulty: Advanced
---

## Statement

Implement a single function that analyzes a route of `(x, y)` points, combining tuple creation, unpacking (including `*`), immutability, and tuples as dictionary keys.

## Theory

This problem introduces no new concepts. It combines this module's topics:

- Read points as tuples and **unpack** each into `x` and `y` in loops.
- Use **extended unpacking** to separate the first and last points from any points in between.
- Use tuples as **dictionary keys** to count how often each cell is visited.
- Return a result made of tuples, including a nested tuple for the bounding box, so the returned structure cannot be altered by the caller.

The Manhattan distance between two points $(x_1, y_1)$ and $(x_2, y_2)$ is:

$$d = |x_2 - x_1| + |y_2 - y_1|$$

No new theory is required beyond re-reading those topics.

## Explanation

`analyze_route` computes the bounding box with a plain loop and running min/max comparisons (per the spec's own "do not use min() or max()" constraint), and gets the first and last points via `first, *_, last = points` — the extended-unpacking idiom this module's second topic introduces, using `_` for the middle section since its contents aren't needed here, only its presence is. The empty-route case is handled as its own early return (`visit_counts`, `path_length`, and the loop-based bounding box all have no sensible value to compute over zero points), matching the spec's explicit `({}, None, 0, 0, 0)`.
