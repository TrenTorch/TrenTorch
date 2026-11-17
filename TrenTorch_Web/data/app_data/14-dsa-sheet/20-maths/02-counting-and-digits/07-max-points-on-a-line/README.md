---
name: sheet-max-points-on-a-line
title: 'Max Points on a Line'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
theory: points-on-one-line
---

## Statement

`points[i] = [x, y]` are **different** points on a plane. Return the **largest number of points that lie on the same straight line**.

For `[[1, 1], [2, 2], [3, 3]]` the answer is `3`; for `[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]` it is `4`.

The starter code tests every triple of points. It is correct but too slow for many points.

### Examples

**Example 1**

Input:

```python
max_points([[1, 1], [2, 2], [3, 3]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]])
```

Output:

```text
4
```

### Constraints

- `0 <= len(points) <= 300`
- `0 <= x, y <= 10000`
- All points are different.

## Explanation

`slopes` counts points by normalised direction from the current point. The best line through it has `max(slopes.values()) + 1` points.

### Complexity

- Time: O(n^2). For each point, every later point is placed in a table by its reduced direction.
- Space: O(n). The table of directions for one point.
